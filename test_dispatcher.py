from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code==200
    assert res.json() == {"status": "ok"}
def test_route_users_to_user_service(monkeypatch):
    import main as dispatcher_main
    def fake_forward(method,url,headers=None,json=None):
        class FakeResp:
            status_code=200
            def json(self):
                return{"id":2,"name":"Test"}
        return FakeResp()
    monkeypatch.setattr(dispatcher_main,"forward_request",fake_forward)
    res=client.get("/users/2")
    assert res.status_code==200
    assert res.json()["id"]==2
