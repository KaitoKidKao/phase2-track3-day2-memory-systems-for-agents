from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

class IntentClassification(BaseModel):
    """Plan to execute based on user intent."""
    intent: Literal["user_preference", "factual_recall", "experience_recall", "general_query"] = Field(
        description="The type of memory retrieval needed."
    )
    reasoning: str = Field(description="Explanation for the choice.")

class MemoryRouter:
    """
    Classifies the user input to route it to the appropriate memory backend.
    """
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.structured_llm = self.llm.with_structured_output(IntentClassification)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intent classifier for a Multi-Memory Agent.
            Categorize the user query into one of these types:
            - user_preference: Queries about user likes, dislikes, habits, or settings (e.g., 'I like spicy food', 'What is my favorite color?').
            - factual_recall: Queries about objective facts or specific data previously stored (e.g., 'What is the capital of France?', 'Recall the project details I gave you').
            - experience_recall: Queries about specific past events or interactions (e.g., 'What did we talk about yesterday regarding the hike?', 'Tell me about my trip to Japan').
            - general_query: Anything else that doesn't require specific memory lookup.
            """),
            ("human", "{query}")
        ])
        
        self.chain = self.prompt | self.structured_llm

    def classify(self, query: str) -> IntentClassification:
        return self.chain.invoke({"query": query})
