from pydantic import BaseModel
from typing import Optional
from datetime import date

class User(BaseModel):
    id: Optional[int] = None  # Default to None
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
    limits: float

class Investment(BaseModel):
    user_id: int
    advice: str
    date: date

class UserInsightsRequest(BaseModel):
    user_id: int
