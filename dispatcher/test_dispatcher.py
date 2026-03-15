from fastapi.testclient import TestClient
import app as dispatcher_app
from fastapi import FastAPI,Request,Response,HTTPException
client = TestClient(dispatcher_app.app)

def test_health():
    res = client.get("/health")
    assert res.status_code==200
    assert res.json() == {"status": "ok"}
def test_route_users_to_user_service(monkeypatch):
    
    def fake_forward(method,url,headers=None,json=None):
        class FakeResp:
            status_code=200
            text ='{"id":2,"name": "Test"}'
        return FakeResp()
    monkeypatch.setattr(dispatcher_app,"forward_request",fake_forward)
    res=client.get("/users/2",headers={"Authorization":"Bearer fake-token"})
    assert res.status_code==200
    assert res.json()["id"]==2
def test_route_products_to_product_service(monkeypatch):
    def fake_forward(method,url, headers=None,json=None):
        class FakeResp:
            status_code=200
            text='{"id":5,"name": "Keyboard", "price":1200}'
        return FakeResp()
    monkeypatch.setattr(dispatcher_app,"forward_request",fake_forward)
    res=client.get("/products/5",headers={"Authorization":"Bearer fake-token"})
    assert res.status_code == 200
    assert res.json()["id"]==5
    assert res.json()["name"] == "Keyboard"
def test_request_without_autharization_header_returns_401():
    res = client.get("/users/2")
    assert res.status_code==401
    assert res.json()["detail"]=="Authorization header missing"
    


