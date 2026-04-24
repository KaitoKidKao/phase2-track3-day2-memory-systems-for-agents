from typing import TypedDict, List, Annotated, Sequence
import operator
import json
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from core.router import MemoryRouter
from core.token_manager import TokenManager
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory
from langchain_openai import ChatOpenAI

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    intent: str
    retrieved_memories: List[str]
    user_id: str
    with_memory: bool

class MultiMemoryGraph:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name)
        self.router = MemoryRouter()
        self.token_manager = TokenManager()
        
        # Initialize memories
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        
        self.workflow = StateGraph(AgentState)
        
        # Define nodes
        self.workflow.add_node("classify", self.classify_node)
        self.workflow.add_node("retrieve", self.retrieve_node)
        self.workflow.add_node("generate", self.generate_node)
        self.workflow.add_node("store", self.store_node) # New node for saving
        
        # Define edges
        self.workflow.set_entry_point("classify")
        self.workflow.add_edge("classify", "retrieve")
        self.workflow.add_edge("retrieve", "generate")
        self.workflow.add_edge("generate", "store") # Save after generating
        self.workflow.add_edge("store", END)
        
        self.app = self.workflow.compile()

    def classify_node(self, state: AgentState):
        if not state.get("with_memory", True):
            return {"intent": "general_query"}
            
        last_message = state["messages"][-1].content
        classification = self.router.classify(last_message)
        return {"intent": classification.intent}

    def retrieve_node(self, state: AgentState):
        if not state.get("with_memory", True):
            return {"retrieved_memories": []}
            
        intent = state["intent"]
        user_id = state["user_id"]
        query = state["messages"][-1].content
        memories = []
        
        if intent == "user_preference":
            prefs = self.long_term.get_user_preferences(user_id)
            if prefs:
                memories.append(f"User Preferences: {prefs}")
        elif intent == "factual_recall":
            facts = self.semantic.query_facts(query)
            memories.extend(facts)
        elif intent == "experience_recall":
            episodes = self.episodic.search_episodes(user_id, query)
            for e in episodes:
                memories.append(f"Past Episode ({e['timestamp']}): {e['content']}")
                
        return {"retrieved_memories": memories}

    def generate_node(self, state: AgentState):
        system_msg = SystemMessage(content="You are a helpful assistant with multi-memory capabilities. Use the provided context and history to answer accurately. If the user introduces themselves or shares a preference, acknowledge it.")
        
        # Trim context (includes history now)
        messages_to_send = self.token_manager.trim_context(
            system_msg, 
            state["messages"], 
            state.get("retrieved_memories", [])
        )
        
        response = self.llm.invoke(messages_to_send)
        return {"messages": [response]}

    def store_node(self, state: AgentState):
        """Saves information to memory based on intent using LLM extraction."""
        if not state.get("with_memory", True):
            return {}
            
        intent = state["intent"]
        user_id = state["user_id"]
        last_query = [m for m in state["messages"] if isinstance(m, HumanMessage)][-1].content
        
        # If the user is providing info, try to extract facts
        if intent in ["user_preference", "general_query"]:
            extract_prompt = f"""Extract any user preferences, personal facts, or experiences from the following message.
            Format as a JSON list of objects with 'type' (preference or experience), 'key' (e.g., 'allergy', 'name', 'hobby'), and 'value'.
            Message: "{last_query}"
            Return ONLY the JSON list."""
            
            try:
                raw_extraction = self.llm.invoke(extract_prompt).content
                # Very basic cleanup for JSON parsing
                if "[" in raw_extraction and "]" in raw_extraction:
                    json_str = raw_extraction[raw_extraction.find("["):raw_extraction.rfind("]")+1]
                    extracted_facts = json.loads(json_str)
                    
                    for fact in extracted_facts:
                        if fact['type'] == 'preference':
                            # This handles conflicts by overwriting the same key in Redis
                            self.long_term.set_user_preference(user_id, fact['key'], fact['value'])
                        else:
                            self.episodic.add_episode(user_id, f"{fact['key']}: {fact['value']}")
            except Exception as e:
                print(f"Extraction failed: {e}")
                
        return {}

    def run(self, user_id: str, message: str, with_memory: bool = True, history: List[BaseMessage] = None):
        inputs = {
            "messages": (history or []) + [HumanMessage(content=message)],
            "user_id": user_id,
            "with_memory": with_memory
        }
        return self.app.invoke(inputs)
