from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

class ShortTermMemory:
    """
    Handles immediate conversation context (recent messages).
    """
    def __init__(self, k: int = 5):
        self.k = k
        self.messages: List[BaseMessage] = []

    def add_message(self, message: BaseMessage):
        self.messages.append(message)
        # We keep all messages here, but the trimmer will handle the actual window
        # for the LLM prompt. This serves as the raw buffer.

    def get_context(self) -> List[BaseMessage]:
        return self.messages[-self.k:]

    def clear(self):
        self.messages = []
