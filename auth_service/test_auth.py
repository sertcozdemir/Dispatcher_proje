from fastapi.testclient import TestClient
from main import app
client=TestClient(app)
def test_login_success():
    res=client.post("/login",json={"username":"admin","password":"1234"})
    assert res.status_code==200
    assert res.json()["access_token"]=="mysecrettoken"
    assert res.json()["token_type"]=="bearer"
def test_login_fail():
    res=client.post("/login",json={"username":"admin","password":"wrong"})
    assert res.status_code==401
    assert res.json()["detail"]=="Invalid username or password"
def test_validate_token_success():
    res=client.post("/validate",json={"token":"mysecrettoken"})
    assert res.status_code==200
    assert res.json()["valid"] is True
def test_validate_token_fail():
    res=client.post("/validate",json={"token":"wrongtoken"})
    assert res.status_code==401
    assert res.json()["detail"]=="Invalid Token"