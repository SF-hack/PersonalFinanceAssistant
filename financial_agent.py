# financial_agent.py
from uagents import Agent

class FinancialAgent(Agent):
    def __init__(self, user_id, user_budget_limits):
        super().__init__(name=f"FinancialAgent-{user_id}")
        self.user_id = user_id
        self.user_budget_limits = user_budget_limits

    def analyze_data(self, data):
        total_expense = sum(expense['amount'] for expense in data)
        overspending_categories = {}

        for expense in data:
            category = expense['category']
            if category not in overspending_categories:
                overspending_categories[category] = 0
            overspending_categories[category] += expense['amount']

        insights = {
            "total_expense": total_expense,
            "overspending_categories": {
                category: amount
                for category, amount in overspending_categories.items() 
                if amount > self.user_budget_limits.get(category, 0)
            }
        }
        return insights
