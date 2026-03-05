from fastapi.testclient import TestClient
from main import app
import main,pytest
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
    client.post("/users", json={"id": 2, "name": "Test"})
    response = client.get("/users/2")
    assert response.status_code == 200
    assert response.json()["id"] == 2

def test_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404