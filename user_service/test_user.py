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
    def fake_forward(method, url, headers=None,json=None):
        class FakeResp:
            status_code=200
            text='{"id":2,"name":"Test"}'
        return FakeResp()
    def fake_validate(token):
        return True
    monkeypatch.setattr(dispatcher_app,"forward_request",fake_forward)
    monkeypatch.setattr(dispatcher_app,"is_token_valid",fake_validate)
    res=client.get("/users/2",headers={"Authorization":"Bearer validtoken"})
    assert res.status_code==200
    assert res.json()["id"]