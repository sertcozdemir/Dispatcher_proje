from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Dict
from pymongo import MongoClient

app=FastAPI()

client= MongoClient("mongodb://localhost:27017/")
db = client["user_db"]
collection=db["users"]

class User(BaseModel):
    id:int
    name:str
@app.post("/users",status_code=201)
def create_user(user: User):
    if collection.find_one({"id": user.id}):
        raise HTTPException(status_code=400, detail="User already exists")
    collection.insert_one(user.model_dump())
    return user
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = collection.find_one({"id": user_id}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user