from fastapi import FastAPI
import requests
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import hashlib

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello world!"}

@app.get("/method")
def method():
    return JSONResponse(content={"method": "GET"},status_code=200)


@app.put("/method")
def method():
    return JSONResponse(content={"method": "PUT"},status_code=200)

@app.options("/method")
def method():
    return JSONResponse(content={"method": "OPTIONS"},status_code=200)

@app.delete("/method")
def method():
    return JSONResponse(content={"method": "DELETE"},status_code=200)

@app.post("/method")
def method():
    return JSONResponse(content={"method": "POST"},status_code=201)

@app.get("/auth")
def auth(password,password_hash):
    sha512_hash = hashlib.sha512()
    sha512_hash.update(bytes(password, encoding="ASCII"))
    m = sha512_hash.hexdigest()
    if m == password_hash:
        return JSONResponse(status_code=204)
    else:
        return JSONResponse(status_code=401)

class Item(BaseModel):
    name: str
    surname: str

@app.post("/register")
async def register(item: Item):
    content={
        "id": 1,
        "name": item.name,
        "surname": item.surname,
        "register_date": "2021-04-01",
        "vaccination_date": "2021-04-09"
    }
    return JSONResponse(content=content,status_code=201)
