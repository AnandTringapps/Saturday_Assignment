from fastapi import FastAPI, HTTPException
from typing import List, Dict
from collections import deque

class RecommendationSystem:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    def _initialize(self):
        self.data = {
          "users": [
            {
              "id": 1,
              "name": "Alice",
              "preferences": [1, 3, 5]
            },
            {
              "id": 2,
              "name": "Bob",
              "preferences": [2, 4, 6]
            }
          ],
          "items": [
            {
              "id": 1,
              "name": "Item 1",
              "relatedItems": [2, 3]
            },
            {
              "id": 2,
              "name": "Item 2",
              "relatedItems": [1, 4]
            },
            {
              "id": 3,
              "name": "Item 3",
              "relatedItems": [1, 5]
            },
            {
              "id": 4,
              "name": "Item 4",
              "relatedItems": [2, 6]
            },
            {
              "id": 5,
              "name": "Item 5",
              "relatedItems": [3, 6]
            },
            {
              "id": 6,
              "name": "Item 6",
              "relatedItems": [4, 5]
            }
          ]
        }
    def recommend_items(self, user_id: int) -> Dict[str, List[dict]]:
     user = next((u for u in self.data["users"] if u["id"] == user_id), None)
     if user is None:
        raise HTTPException(status_code=404, detail="User not found")
     user_preferences = user["preferences"]
     visited = set(user_preferences)
     queue = deque(user_preferences)
     while queue:
        item_id = queue.popleft()
        for item in self.data["items"]:
            if item["id"] == item_id:
                related_items = set(item["relatedItems"]) - visited
                visited.update(related_items)
                queue.extend(related_items)
     recommended_items = [
        {
            "id": item["id"],
            "name": item["name"],
            "relatedItems": list(set(item["relatedItems"]) & visited)
        }
        for item in self.data["items"] 
        if item["id"] in visited and item["id"] not in user_preferences
     ]
     return {
        "user": {"name": user["name"], "preferences": user_preferences},
        "recommended_items": recommended_items
    }
app = FastAPI()
recommendation_system = RecommendationSystem()

@app.get("/recommend/{user_id}")
async def get_recommendations(user_id: int):
    recommendations = recommendation_system.recommend_items(user_id)
    return recommendations
