from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    print(response)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}

def test_method():
    response_get = client.get("/method")
    response_put = client.put("/method")
    response_post = client.post("/method")
    response_options = client.options("/method")
    response_delete = client.delete("/method")
    assert response_get.json() == {"method": "GET"}
    assert response_put.json() == {"method": "PUT"}
    assert response_post.json() == {"method": "POST"}
    assert response_options.json() == {"method": "OPTIONS"}
    assert response_delete.json() == {"method": "DELETE"}