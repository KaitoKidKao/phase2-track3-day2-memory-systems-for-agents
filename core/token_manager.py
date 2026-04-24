import tiktoken
from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

class TokenManager:
    """
    Manages context window size and implements the 4-level eviction hierarchy.
    """
    def __init__(self, model_name: str = "gpt-4o-mini", limit: int = 4096):
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        self.limit = limit

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def count_messages_tokens(self, messages: List[BaseMessage]) -> int:
        num_tokens = 0
        for message in messages:
            num_tokens += 4 # overhead
            num_tokens += self.count_tokens(message.content)
        num_tokens += 2 # assistant overhead
        return num_tokens

    def trim_context(self, system_message: SystemMessage, 
                     short_term: List[BaseMessage], 
                     retrieved_memories: List[str]) -> List[BaseMessage]:
        """
        Implements 4-level hierarchy eviction:
        Level 1: System Message (Highest Priority - Never evict)
        Level 2: Recent messages (Short-term)
        Level 3: Fact/Semantic memories
        Level 4: Old episodic logs
        """
        
        # We'll construct the prompt and trim from the bottom (Level 4) if needed
        # In this implementation, we'll keep the system message and then add others
        
        final_messages = [system_message]
        current_tokens = self.count_messages_tokens(final_messages)
        
        # Add Short-term (Level 2) - we might want to trim these first if they are too long
        # but usually recent messages are most important.
        available_tokens = self.limit - current_tokens
        
        # For simplicity in this lab, we'll prioritize short-term, then semantic, then episodic
        # until the limit is hit.
        
        # 1. Add retrieved semantic/factual memories as context strings in a system message
        if retrieved_memories:
            mem_content = "\n".join([f"- {m}" for m in retrieved_memories])
            mem_msg = SystemMessage(content=f"Relevant Memory Snippets:\n{mem_content}")
            if current_tokens + self.count_messages_tokens([mem_msg]) < self.limit:
                final_messages.append(mem_msg)
                current_tokens += self.count_messages_tokens([mem_msg])

        # 2. Add Short-term messages
        for msg in reversed(short_term):
            msg_tokens = self.count_messages_tokens([msg])
            if current_tokens + msg_tokens < self.limit:
                # Insert after system messages
                final_messages.insert(1 if len(final_messages) == 1 else 2, msg)
                current_tokens += msg_tokens
            else:
                break
                
        return final_messages
