from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.db import Connection
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/registration")
async def registration(obj: Union[dict, None] = None):
    if obj["key"] != os.getenv("SERVICE_AUTH_TOKEN"):
        return {"error": "Invalid key"}
    
    connection = Connection()
    arr = connection.select("person")
    return arr


'''

connection = Connection()
connection.insert("person", ["username", "password"], ["elf", "123456789"])

arr = connection.select("person")
print(arr)

'''