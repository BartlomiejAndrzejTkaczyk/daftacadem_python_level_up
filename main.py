from fastapi import FastAPI
import requests
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": os.environ['REQUEST_METHOD']}

@app.get("/method")
def method():
    return {"method": "GET"}

@app.post("/method")
def method():
    return {"method": "POST"}