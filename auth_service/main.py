from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app=FastAPI()
FAKE_USER = {
    "username": "admin",
    "password": "1234"
}
VALID_TOKEN ="mysecrettoken"
class LoginRequest(BaseModel):
    username:str
    password:str
class TokenRequest(BaseModel):
    token:str
@app.post("/login")
def login(data: LoginRequest):
    if data.username== FAKE_USER["username"] and data.password== FAKE_USER["password"]:
        return {
            "access_token":VALID_TOKEN,
            "token_type":"bearer"
        }   
    raise HTTPException(status_code=401, detail="Invalid username or password")
@app.post("/validate")
def validate_token(data: TokenRequest):
    if data.token==VALID_TOKEN:
        return {"valid":True}
    raise HTTPException(status_code=401,detail="Invalid Token")