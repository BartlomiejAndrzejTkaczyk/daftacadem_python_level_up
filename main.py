from fastapi import FastAPI
import requests
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import hashlib
import datetime

app = FastAPI()
app.counter_id = 1


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

def addDayToDateYMD(date_str:str, days:int, seperator:str = '-'):
    YMD = [int(ele) for ele in date_str.split(seperator)]
    date = datetime.date(YMD[0],YMD[1],YMD[2])
    date += datetime.timedelta(days=days)
    return date

class Item(BaseModel):
    name: str
    surname: str


@app.post("/register")
async def register(item: Item):
    vaccination_date = addDayToDateYMD("2021-04-01",len(item.name + item.surname))
    tday = datetime.date().today()
    content={
        "id": app.counter_id,
        "name": item.name,
        "surname": item.surname,
        "register_date": str(tday),
        "vaccination_date": str(vaccination_date)
    }
    app.counter_id+=1
    return JSONResponse(content=content,status_code=201)
