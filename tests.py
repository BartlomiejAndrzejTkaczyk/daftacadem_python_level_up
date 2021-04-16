from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    print(response)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}