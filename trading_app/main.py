from fastapi import FastAPI
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

app = FastAPI(title="Trading_app")

class TypeDegree(Enum):
    newbi = "newbi"
    expert = "expert"

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: TypeDegree

class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []

fake_users = [
    {"id":1, "role":"admin",  "name": "Aliteya", "degree":[
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]},
    {"id":2, "role":"investor", "name":"Hohich"},
    {"id":3, "role":"trader", "name":"Medianoche"},
]

@app.get("/users/{user_id}", response_model=List[User])
def return_user(user_id: int):
    return [user for user in fake_users if user_id == user.get("id")]

class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=10)
    side: str
    price: float = Field(ge=0)
    amount: int


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "NotCoin", "side": "sell", "price": 1000, "amount": 3.4},
    {"id": 2, "user_id": 2, "currency": "NotCoin", "side": "buy", "price": 1002, "amount": 3.4},
    {"id": 3, "user_id": 2, "currency": "NotCoin", "side": "buy", "price": 1002, "amount": 3.4},
    {"id": 4, "user_id": 2, "currency": "NotCoin", "side": "buy", "price": 1002, "amount": 3.4},
    {"id": 5, "user_id": 3, "currency": "NotCoin", "side": "buy", "price": 1002, "amount": 3.4},
    {"id": 6, "user_id": 3, "currency": "NotCoin", "side": "buy", "price": 1002, "amount": 3.4},
    {"id": 7, "user_id": 3, "currency": "NotCoin", "side": "buy", "price": 1002, "amount": 3.4},
]

@app.get("/trades")
def get_trades(limit: int = 5, offset: int = 0 ):
    return fake_trades[::-1][offset:][:limit]

@app.post("/trades")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}

fake_users2 = [
    {"id":1, "role":"admin",  "name":"Aliteya" },
    {"id":2, "role":"investor",  "name":"Hohich" },
    {"id":3, "role":"trader",  "name":"Medianoche" },
]

@app.post("/users/{user_id}")
def change_user_name(user_id : int, new_name: str):
    curr_user = list(filter(lambda user: user_id == user.get("id"), fake_users2))[0]
    
    curr_user["name"] = new_name
    return {"status": 200, "data": curr_user}