from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from pymongo import MongoClient
from fastapi.responses import JSONResponse

app=FastAPI()

client= MongoClient("mongodb://mongo_user:27017/")
db = client["user_db"]
collection=db["users"]

class User(BaseModel):
    name:str
    email:str
class UserResponse(BaseModel):
    id:int
    name:str
    email:str

@app.post("/users",status_code=201,response_model=UserResponse,responses={201:{"description":"User Created Succesfully"}}, summary="Create User")
def create_user(user: User):
    last_user=collection.find_one(sort=[("id",-1)])
    new_id=1 if last_user is None else last_user["id"] + 1

    new_user={
        "id":new_id,
        "name":user.name,
        "email":user.email
    }
    result = collection.insert_one(new_user)
    print("INSERTED ID:",result.inserted_id)
    print("INSERTED DOC:",new_user)
    new_user["_id"]= str(result.inserted_id)
    new_user.pop("_id",None)
    return {
        "id": new_id,
        "name":user.name,
        "email":user.email
    }
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = collection.find_one({"id": user_id}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user