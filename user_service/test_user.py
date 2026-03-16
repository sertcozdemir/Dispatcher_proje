from fastapi.testclient import TestClient
from user_service.main import app
import user_service.main as main,pytest
client = TestClient(app)
@pytest.fixture(autouse=True)
def clean_db():
    main.collection.delete_many({})
    # debug: gerçekten silinmiş mi?
    assert main.collection.count_documents({}) == 0
    yield
    main.collection.delete_many({})

def test_create_user():
    response = client.post("/users", json={"id": 1, "name": "Seto"})
    print("STATUS:", response.status_code)
    print("BODY:", response.text)
    assert response.status_code == 201
    assert response.json()["name"] == "Seto"

def test_get_user():
    client.post("/users", json={"id": 2, "name": "Nilay"})
    response = client.get("/users/2")
    assert response.status_code == 200
    assert response.json()["id"] == 2

def test_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
def test_route_users_to_user_service(monkeypatch):
    def fake_post(url, headers=None,json=None):
        class FakeAuthResp:
            status_code=200
        return FakeAuthResp()
    def fake_request(method,url, headers=None, json=None,timeout=None):
        class FakeUserResp:
            status_code=200
            text='{"id":2,"name":"Test"}'
        return FakeUserResp()
    monkeypatch.setattr(dispatcher_app.httpx,"post",fake_post)
    monkeypatch.setattr(dispatcher_app.httpx,"is_token_valid",fake_request)
    res=client.get("/users/2",headers={"Authorization":"Bearer validtoken"})
    assert res.status_code==200
    assert res.json()["id"]==2