from fastapi import FastAPI
import requests
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import hashlib
import datetime
import json

app = FastAPI()
app.counter_id = 1
app.patients = []

@app.get("/")
def root():
    return {'message': 'Hello world!'}

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

# ---------------

def addDayToDateYMD(date_str:str, days:int, seperator:str = '-'):
    YMD = [int(ele) for ele in date_str.split(seperator)]
    date = datetime.date(YMD[0],YMD[1],YMD[2])
    date += datetime.timedelta(days=days)
    return date

class Item(BaseModel):
    name: str
    surname: str

class Patient:

    def __init__(self, name, surname, tday=datetime.date.today()):
        self.id = app.counter_id
        app.counter_id+=1
        self.name = name
        self.surname = surname
        self.register_date = tday
        self.vaccination_date = addDayToDateYMD(str(tday),len(self.name + self.surname))
    
    def dataInDict(self):
        return {
        "id": self.id,
        "name": self.name,
        "surname": self.surname,
        "register_date": str(self.register_date),
        "vaccination_date": str(self.vaccination_date)
        }
    
    def __str__(self):
        ans = [ele for ele in self.dataInDict().values()]
        return str(ans)

@app.post("/register")
async def register(item: Item):
    patient = Patient(item.name,item.surname)
    app.patients.append(patient)
    return JSONResponse(content=patient.dataInDict(),status_code=201)

@app.get("/patient/{id}")
def get_patient_id(id: int):
    if id<1: return JSONResponse(status_code=400)

    for patient in app.patients:
        if patient.id == id:
            return JSONResponse(content=patient.dataInDict(),status_code=200)
    
    return JSONResponse(status_code=404)