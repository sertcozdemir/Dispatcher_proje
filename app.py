from fastapi import FastAPI, Request, Response,HTTPException,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
app=FastAPI() # api gateway
security=HTTPBearer()
USER_SERVICE_BASE="http://localhost:8001" # user service mikroservis adresi
PRODUCT_SERVICE_BASE="http://localhost:8002"
AUTH_SERVICE_BASE="http://localhost:8003"
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