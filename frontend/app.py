import streamlit as st
import requests

# Title of the app
st.title("AI Personal Finance Assistant")

# Section to add a user
st.header("Add User")
username = st.text_input("Username")
if st.button("Add User"):
    response = requests.post("http://127.0.0.1:8000/add-user/", json={"username": username})
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Error adding user")

# Section to add an expense
st.header("Add Expense")
user_id = st.number_input("User ID", min_value=1)
expense_name = st.text_input("Expense Name")
expense_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
expense_category = st.text_input("Category")
expense_date = st.date_input("Date")

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
        st.error("Error adding expense")
