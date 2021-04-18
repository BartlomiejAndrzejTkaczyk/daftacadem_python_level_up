from fastapi.testclient import TestClient
import hashlib
from main import app
import requests
from pydantic import BaseModel
import json
import pytest
import datetime

client = TestClient(app)

class structurOfGlobalVar:
    test_register_counter_id = 1


gv = structurOfGlobalVar


# root:

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}

# wykrywanie metody

def test_method():
    response_get = client.get("/method")
    response_put = client.put("/method")
    response_post = client.post("/method")
    response_options = client.options("/method")
    response_delete = client.delete("/method")
    assert response_get.json() == {"method": "GET"}
    assert response_get.status_code == 200

    assert response_put.json() == {"method": "PUT"}
    assert response_put.status_code == 200

    assert response_post.json() == {"method": "POST"}
    assert response_post.status_code == 201  # for post is 201! not 201

    assert response_options.json() == {"method": "OPTIONS"}
    assert response_options.status_code == 200

    assert response_delete.json() == {"method": "DELETE"}
    assert response_delete.status_code == 200

# sprawdzania szyforwania

def test_auth_hash():
    password = ["abcd", "hgdaa", "hvsu", "jhuhujvds"]

    for ele in password:
        sha512_hash = hashlib.sha512()
        sha512_hash.update(bytes(ele, encoding="ASCII"))
        password_hash = sha512_hash.hexdigest()
        response = client.get(f"/auth?password={ele}&password_hash={password_hash}")
        assert response.status_code == 204
        response = client.get(f"/auth?password={ele}a&password_hash={password_hash}")
        assert response.status_code == 401

    # test dla zadanych wartsci
    password = "haslo"
    password_hash = "013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215"
    sha512_hash = hashlib.sha512()
    sha512_hash.update(bytes(password, encoding="ASCII"))
    assert sha512_hash.hexdigest() == password_hash

    password = "haslo"
    password_hash = "f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091"
    sha512_hash = hashlib.sha512()
    sha512_hash.update(bytes(password, encoding="ASCII"))
    assert sha512_hash.hexdigest() != password_hash



# sprawdzanie dodawania nowych pacjetow

def addDayToDateYMD(date_str: str, days: int, seperator: str = '-'):
    YMD = [int(ele) for ele in date_str.split(seperator)]
    date = datetime.date(YMD[0], YMD[1], YMD[2])
    date += datetime.timedelta(days=days)
    return date

@pytest.mark.parametrize("name", ["Zenek", "Marek", "Alojzy"])
@pytest.mark.parametrize("surname", ["Nowak", "Kowalczyk", "Tkacz"])
def test_register(name: str, surname: str):
    data = {"name": name, "surname": surname}
    tday = datetime.date.today()
    vaccination_date = addDayToDateYMD(str(tday), len(name + surname))
    respons = {
        "id": gv.test_register_counter_id,
        "name": name,
        "surname": surname,
        "register_date": str(tday),
        "vaccination_date": str(vaccination_date)
    }

    gv.test_register_counter_id += 1
    r = client.post("/register", data=json.dumps(data))

    assert r.json() == respons
    assert r.status_code == 201


# sprawdzanie odczytwania pacjetow:
SIZE_OF_APP_PATIENTS = 9
@pytest.mark.parametrize("id", [index for index in range(1,SIZE_OF_APP_PATIENTS+1)])
def test_get_patient_id(id: int):
    r = client.get(f"/patient/{id}")
    expected_code = 200
    assert r.status_code == expected_code
    assert r.json() == app.patients[id-1].dataInDict()

@pytest.mark.parametrize("id", [index for index in range(SIZE_OF_APP_PATIENTS+2,20)])
def test_get_patient_id(id: int):
    r = client.get(f"/patient/{id}")
    expected_code = 404
    assert r.status_code == expected_code

def test_get_patient_id():
    id = -1
    r = client.get(f"/patient/{id}")
    expected_code = 400
    assert r.status_code == expected_code