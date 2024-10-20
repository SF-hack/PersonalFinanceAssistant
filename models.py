from pydantic import BaseModel
from typing import Optional
from datetime import date

class User(BaseModel):
    id: Optional[int]
    username: str

class Expense(BaseModel):
    user_id: int
    name: str
    amount: float
    category: str
    date: date

class Budget(BaseModel):
    user_id: int
    category: str
    limit: float

class Investment(BaseModel):
    user_id: int
    advice: str
    date: date