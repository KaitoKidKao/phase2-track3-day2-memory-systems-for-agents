import redis
import json
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class LongTermMemory:
    """
    Handles persistent user preferences and long-term facts using Redis.
    """
    def __init__(self):
        host = os.getenv("REDIS_HOST", "localhost")
        port = int(os.getenv("REDIS_PORT", 6379))
        password = os.getenv("REDIS_PASSWORD", None)
        
        try:
            self.client = redis.Redis(
                host=host, 
                port=port, 
                password=password, 
                decode_responses=True
            )
            # Test connection
            self.client.ping()
        except Exception as e:
            print(f"Warning: Redis connection failed: {e}. Using mock storage.")
            self.client = None
            self.mock_storage = {}

    def set_user_preference(self, user_id: str, key: str, value: Any):
        if self.client:
            self.client.hset(f"user:{user_id}:prefs", key, json.dumps(value))
        else:
            if user_id not in self.mock_storage:
                self.mock_storage[user_id] = {}
            self.mock_storage[user_id][key] = value

    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        if self.client:
            data = self.client.hgetall(f"user:{user_id}:prefs")
            return {k: json.loads(v) for k, v in data.items()}
        return self.mock_storage.get(user_id, {})

    def get_preference(self, user_id: str, key: str) -> Optional[Any]:
        if self.client:
            val = self.client.hget(f"user:{user_id}:prefs", key)
            return json.loads(val) if val else None
        return self.mock_storage.get(user_id, {}).get(key)
