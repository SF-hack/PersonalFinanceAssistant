from fastapi import FastAPI, HTTPException
from models import User, Expense, Budget, Investment, UserInsightsRequest
from database import get_connection
from financial_agent import FinancialAgent

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

# Get all users
@app.get("/users/", response_model=list[User])
async def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": user[0], "username": user[1]} for user in users]

# Get all expenses
@app.get("/expenses/", response_model=list[Expense])
async def get_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, amount, category, date FROM expenses")
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"user_id": expense[0], "name": expense[1], "amount": expense[2], "category": expense[3], "date": expense[4]} for expense in expenses]

@app.post("/add-budget/", response_model=dict)
async def add_budget(budget: Budget):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO budgets (user_id, category, limits) VALUES (%s, %s, %s)", 
                   (budget.user_id, budget.category, budget.limits))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Budget added successfully!"}

@app.get("/budgets/", response_model=list[Budget])
async def get_budgets():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, category, limits FROM budgets")
    budgets = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"user_id": budget[0], "category": budget[1], "limits": budget[2]} for budget in budgets]

@app.get("/check-budget/{user_id}", response_model=dict)
async def check_budget(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Get total expenses for the user
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = %s", (user_id,))
    total_expenses = cursor.fetchone()[0] or 0  # Handle case where there are no expenses

    # Get budgets for the user
    cursor.execute("SELECT category, `limits` FROM budgets WHERE user_id = %s", (user_id,))
    budgets = cursor.fetchall()

    # Check if expenses exceed budget for each category
    budget_status = {}
    for category, limit in budgets:
        # Ensure total_expenses and limit are floats
        budget_status[category] = {
            "total_expenses": float(total_expenses),  # Convert to float
            "limits": float(limit),  # Ensure limit is treated as a float
            "exceeds": total_expenses > limit,
        }

    cursor.close()
    conn.close()
    return {"user_id": user_id, "budgets": budget_status}

@app.get("/get-expenses/{user_id}", response_model=dict)
async def get_expenses(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT category, amount, date FROM expenses WHERE user_id = %s", (user_id,))
    expenses = cursor.fetchall()

    cursor.close()
    conn.close()

    expense_list = [{"category": row[0], "amount": row[1], "date": row[2]} for row in expenses]
    return {"user_id": user_id, "expenses": expense_list}

@app.post("/financial-insights/")
async def financial_insights(request: UserInsightsRequest):
    user_id = request.user_id
    # Fetch user expenses and budget limits from the database
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT category, amount FROM expenses WHERE user_id = %s", (user_id,))
    expenses = cursor.fetchall()
    
    user_expenses = [{"category": row[0], "amount": row[1]} for row in expenses]
    
    cursor.execute("SELECT category, limits FROM budgets WHERE user_id = %s", (user_id,))
    budget_limits = cursor.fetchall()
    user_budget_limits = {row[0]: row[1] for row in budget_limits}

    # Initialize and use the Uagent
    agent = FinancialAgent(user_id, user_budget_limits)
    insights = agent.analyze_data(user_expenses)

    cursor.close()
    conn.close()
    
    return insights



