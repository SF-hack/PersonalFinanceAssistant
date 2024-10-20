from fastapi import FastAPI, HTTPException
from models import User, Expense, Budget, Investment
from database import get_connection

app = FastAPI()

@app.post("/add-user/")
async def add_user(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (user.username,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User added successfully!"}

@app.post("/add-expense/")
async def add_expense(expense: Expense):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (user_id, name, amount, category, date) VALUES (%s, %s, %s, %s, %s)", 
                   (expense.user_id, expense.name, expense.amount, expense.category, expense.date))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Expense added successfully!"}

# You can continue to add more endpoints for budgets and investments...
