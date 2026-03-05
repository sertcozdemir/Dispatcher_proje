from fastapi.testclient import TestClient
import app as dispatcher_app
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
    res=client.get("/users/2")
    assert res.status_code==200
    assert res.json()["id"]==2
