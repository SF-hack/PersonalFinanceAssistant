import streamlit as st
import requests

# Title of the app
st.title("AI Personal Finance Assistant")

# Section to add a user
st.header("Add User")
username = st.text_input("Username", key="username_input")
if st.button("Add User"):
    if username:
        response = requests.post("http://127.0.0.1:8000/add-user/", json={"username": username})
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error("Error adding user: " + response.text)
    else:
        st.error("Username cannot be empty.")

# Section to view users
st.header("View Users")
if st.button("Refresh Users"):
    user_response = requests.get("http://127.0.0.1:8000/users/")
    if user_response.status_code == 200:
        users = user_response.json()
        st.write(users)
    else:
        st.error("Error fetching users")

# Section to add an expense
st.header("Add Expense")
user_id = st.number_input("User ID", min_value=1, key="expense_user_id")
expense_name = st.text_input("Expense Name", key="expense_name")
expense_amount = st.number_input("Amount", min_value=0.0, format="%.2f", key="expense_amount")
expense_category = st.text_input("Category", key="expense_category")
expense_date = st.date_input("Date", key="expense_date")

if st.button("Add Expense"):
    expense_data = {
        "user_id": user_id,
        "name": expense_name,
        "amount": expense_amount,
        "category": expense_category,
        "date": str(expense_date)
    }
    response = requests.post("http://127.0.0.1:8000/add-expense/", json=expense_data)
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Error adding expense: " + response.text)

# Section to view expenses
st.header("View Expenses")
if st.button("Refresh Expenses"):
    expense_response = requests.get("http://127.0.0.1:8000/expenses/")
    if expense_response.status_code == 200:
        expenses = expense_response.json()
        st.write(expenses)
    else:
        st.error("Error fetching expenses")

# Section to add a budget
st.header("Add Budget")
budget_user_id = st.number_input("User ID", min_value=1, key="budget_user_id")
budget_category = st.text_input("Category", key="budget_category")
budget_limit = st.number_input("Limit", min_value=0.0, format="%.2f", key="budget_limit")

if st.button("Add Budget"):
    budget_data = {
        "user_id": budget_user_id,
        "category": budget_category,
        "limits": budget_limit
    }
    response = requests.post("http://127.0.0.1:8000/add-budget/", json=budget_data)
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Error adding budget: " + response.text)

# Section to view budgets
st.header("View Budgets")
if st.button("Refresh Budgets"):
    budget_response = requests.get("http://127.0.0.1:8000/budgets/")
    if budget_response.status_code == 200:
        budgets = budget_response.json()
        st.write(budgets)
    else:
        st.error("Error fetching budgets")

# Section to check budget status
st.header("Check Budget Status")
check_user_id = st.number_input("User ID to Check Budget", min_value=1)

if st.button("Check Budget"):
    response = requests.get(f"http://127.0.0.1:8000/check-budget/{check_user_id}")
    if response.status_code == 200:
        budget_info = response.json()
        st.write(f"Budget status for User ID: {budget_info['user_id']}")
        for category, status in budget_info["budgets"].items():
            st.write(f"Debug: Total Expenses: {status['total_expenses']}, Limits: {status['limits']}")  # Debugging line
            status_message = "Within limit" if not status["exceeds"] else "Exceeds limit"
            st.write(f"{category}: ${status['total_expenses']:.2f} (Limit: ${status['limits']:.2f}) - {status_message}")
    else:
        st.error("Error checking budget: " + response.text)

