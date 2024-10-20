from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Temporary in-memory storage for user data
user_data = {
    "user123": {
        "budget": 1000,
        "expenses": [],
        "investment_advice": None
    }
}

# Define a Pydantic model for expense data
class ExpenseData(BaseModel):
    user_id: str
    data: dict

@app.post("/store_expense_data/")
async def store_expense_data(expense_data: ExpenseData):
    user_id = expense_data.user_id
    data = expense_data.data
    if user_id not in user_data:
        user_data[user_id] = {"budget": 0, "expenses": [], "investment_advice": None}
    
    user_data[user_id]["expenses"].append(data)
    return {"status": "success", "user_data": user_data[user_id]}

# Other endpoints remain unchanged
@app.get("/get_expense_data/{user_id}")
async def get_expense_data(user_id: str):
    data = user_data.get(user_id, {}).get("expenses", [])
    return {"expenses": data}

@app.post("/store_investment_advice/")
async def store_investment_advice(user_id: str, advice: str):
    user_data[user_id]["investment_advice"] = advice
    return {"status": "success"}

@app.get("/get_investment_advice/{user_id}")
async def get_investment_advice(user_id: str):
    advice = user_data.get(user_id, {}).get("investment_advice", "No advice available")
    return {"investment_advice": advice}
