import json
import os
from datetime import datetime
from typing import List, Dict, Any

class EpisodicMemory:
    """
    Handles episodic logs (specific experiences or events) stored in a JSON file.
    """
    def __init__(self, file_path: str = "data/episodic_logs.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def add_episode(self, user_id: str, content: str, metadata: Dict[str, Any] = None):
        episode = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "content": content,
            "metadata": metadata or {}
        }
        
        episodes = self.get_all_episodes(user_id)
        episodes.append(episode)
        
        # In a real app, we might want to lock this file or use a DB
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(episodes, f, indent=2, ensure_ascii=False)

    def get_all_episodes(self, user_id: str) -> List[Dict[str, Any]]:
        if not os.path.exists(self.file_path):
            return []
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            try:
                all_episodes = json.load(f)
                return [e for e in all_episodes if e.get("user_id") == user_id]
            except json.JSONDecodeError:
                return []

    def search_episodes(self, user_id: str, query: str) -> List[Dict[str, Any]]:
        # Simple keyword search for episodic memory if not using vector DB for this
        episodes = self.get_all_episodes(user_id)
        results = [e for e in episodes if query.lower() in e["content"].lower()]
        return results[-3:] # Return last 3 relevant episodes
