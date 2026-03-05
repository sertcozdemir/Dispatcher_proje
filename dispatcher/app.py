from fastapi import FastAPI, Request, Response
import httpx
app=FastAPI()
USER_SERVICE_BASE="http://localhost:8001"
def forward_request(method:str,url:str,headers=None,json=None):
    return httpx.request(method,url,headers=headers,json=json,timeout=5.0)
@app.get("/health")
def health():
    return {"status":"ok"}
@app.get("/users/{user_id}")
def proxy_get_user(user_id: int,request:Request):
    upstream_url=f"{USER_SERVICE_BASE}/users/{user_id}"
    r = forward_request("GET",upstream_url,headers=dict(request.headers))
    return Response(content=r.text,status_code=r.status_code,media_type="application/json")
