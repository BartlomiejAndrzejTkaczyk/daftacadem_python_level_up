from fastapi import FastAPI
import requests
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello world!"}

@app.get("/method")
def method():
    return {"method": "GET"}

@app.put("/method")
def method():
    return {"method": "PUT"}

@app.options("/method")
def method():
    return {"method": "OPTIONS"}

@app.delete("/method")
def method():
    return {"method": "DELETE"}

@app.post("/method")
def method():
    return {"method": "POST"}