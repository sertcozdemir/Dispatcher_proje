from fastapi import FastAPI, Request, Response,HTTPException,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from pydantic import BaseModel, Field

app=FastAPI() # api gateway
security=HTTPBearer()
USER_SERVICE_BASE="http://user_service:8001" # user service mikroservis adresi
PRODUCT_SERVICE_BASE="http://product_service:8002"
AUTH_SERVICE_BASE="http://auth_service:8003"
class UserCreate(BaseModel):
    name:str= Field(...,min_length=1,max_length=100)
    email:str
class ProductCreate(BaseModel):
    name:str=Field(...,min_length=1,max_length=100)
    price:float=Field(...,gt=0)
    stock:int=Field(...,ge=0)
    category:str=Field(...,min_length=1,max_length=50)
class ProductResponse(BaseModel):
    id:int
    name:str
    price:float
    stock:int
    category:str
class UserResponse(BaseModel):
    id: int
    name:str
    email:str
def forward_request(method:str,url:str,headers=None,json=None):
    return httpx.request(method,url,headers=headers,json=json,timeout=5.0) #Başka bir servise istek gönderir
def is_token_valid(token: str) -> bool:
    response=httpx.post(
        f"{AUTH_SERVICE_BASE}/validate",
        json={"token":token},
        timeout=5.0
    )# auth service e token geçerli mi so rusu 200 true 401 false 
    return response.status_code==200
@app.get("/health")
def health():
    return {"status":"ok"} # servis calısıyor mu kontrolü
@app.get("/users/{user_id}")
def proxy_get_user(user_id:int,request:Request,credentials:HTTPAuthorizationCredentials=Depends(security)):
    validate_auth_header(credentials)
    upstream_url=f"{USER_SERVICE_BASE}/users/{user_id}"
    r = forward_request("GET",upstream_url,headers=dict(request.headers))
    return Response(content=r.text,status_code=r.status_code,media_type="application/json")
@app.get("/products/{product_id}")
def proxy_get_product(product_id: int,request:Request,credentials:HTTPAuthorizationCredentials=Depends(security)):
    validate_auth_header(credentials)
    upstream_url = f"{PRODUCT_SERVICE_BASE}/products/{product_id}"
    r=forward_request("GET",upstream_url,headers=dict(request.headers))
    return Response(content=r.text,status_code=r.status_code,media_type="application/json")
@app.post("/users",
          status_code=201,
          response_model=UserResponse,
          responses={
              201:{"description":"User created successfully"},
              401:{"description":"Unauthorized"},
              503:{"description":"Upstream service unavailable"}
          },summary="Create user via dispatcher")

def create_user(user:UserCreate,request:Request,credentials:HTTPAuthorizationCredentials=Depends(security)):

    validate_auth_header(credentials)
    upstream_url=f"{USER_SERVICE_BASE}/users"
    headers=dict(request.headers)
    headers.pop("host",None)
    headers.pop("content-length",None)
    r=forward_request("POST",upstream_url,headers=headers,json=user.model_dump())
    return r.json()
@app.post("/products",responses={
    201:{"description":"Product Created Successfully"}
})
def create_product(product:ProductCreate,request:Request,credentials:HTTPAuthorizationCredentials=Depends(security)):
    validate_auth_header(credentials)
    upstream_url=f"{PRODUCT_SERVICE_BASE}/products"
    headers=dict(request.headers)
    headers.pop("host",None)
    headers.pop("content-length",None)
    r=forward_request("POST",upstream_url,headers=headers,json=product.model_dump())
    return Response(content=r.text, status_code=r.status_code,media_type="application/json")
    
def validate_auth_header(credentials: HTTPAuthorizationCredentials=Depends(security)):
    auth_header=credentials.scheme+ " " + credentials.credentials
    if not auth_header:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )
    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization format"
        )
    token= credentials.credentials
    if not is_token_valid(token):
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )