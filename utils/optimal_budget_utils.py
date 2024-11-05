import streamlit as st
from pulp import *
from typing import Dict, List, Optional
import pandas as pd
from database.db_config import get_connection
import datetime

date = datetime.date.today()
month = datetime.datetime.now().month
year = datetime.datetime.now().year
columns = [ "Income","Savings","Rent", "Groceries", "Shopping", "Daily_spending","Loan", "Bills", "Others"]
email = st.session_state.email

def load_optimal_budget():
    conn = get_connection()
    cursor = conn.cursor(buffered=True)
    query = "SELECT income,savings,rent,groceries,shopping,daily_spending,loan,bills,other_expenses FROM optimalbudget WHERE email = %s AND created_month = %s AND created_year = %s"
    cursor.execute(query,(email,month,year))
    values = cursor.fetchone()
    return values

def insert_optimal_budget():
    conn = get_connection()
    cursor = conn.cursor(buffered= True)
    income = st.session_state.income
    optimal_budget = st.session_state.optimal_budget
    savings = optimal_budget["Savings"]
    rent = optimal_budget["Rent"]
    groceries = optimal_budget["Groceries"]
    shopping = optimal_budget["Shopping"]
    daily_spending = optimal_budget["Daily_spending"]
    loan = optimal_budget["Loan"]
    bills = optimal_budget["Bills"]
    other_expenses = optimal_budget["Others"]
    query = "INSERT INTO optimalbudget (email, tracked_date,created_month,created_year,income,savings,rent,groceries,shopping,daily_spending,loan,bills,other_expenses) VALUES (%s,%s,%s,%s,%s,%s ,%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query,(email,date,month,year,income,savings,rent,groceries,shopping,daily_spending,loan,bills,other_expenses))
    conn.commit()
    cursor.close()
    conn.close()


class BudgetOptimizer:
    def __init__(self):
        self.expense_categories = [
            "Rent", "Groceries", "Shopping", "Daily_spending",
            "Loan", "Bills", "Others"
        ]
        
    def optimize_budget(
        self,
        income: float,
        expense_dict: Dict[str, float],
        min_spendings: List[str],
        savings_goal: float
    ) -> Optional[Dict[str, float]]:
        """
        Optimize budget to maximize savings while respecting expense constraints
        
        Args:
            income: Total monthly income
            expense_dict: Dictionary of expense categories and their maximum amounts
            min_spendings: List of expense categories to minimize
            savings_goal: Minimum required savings
        
        Returns:
            dict: Optimized spending amounts for each category and savings
        """
        # Create the optimization problem
        prob = LpProblem("Budget_Optimization", LpMaximize)
        
        # Create decision variables for each expense category
        spending_vars = {}
        for category, max_amount in expense_dict.items():
            if max_amount > 0:
                spending_vars[category] = LpVariable(f"spend_{category}", 0, max_amount)
        
        # Create savings variable
        savings = LpVariable("savings", savings_goal)  # Allow for higher savings
        
        # Objective: Maximize savings while minimizing selected categories
        optimization_expr = savings - 0.01 * lpSum(
            spending_vars[category] for category in min_spendings if category in spending_vars
        )
        prob += optimization_expr
        
        # Constraint: Total spending + savings must equal income
        prob += lpSum(spending_vars.values()) + savings == income
        
        # Minimum spending constraints
        essential_categories = ["Rent", "Groceries", "Bills", "Loan"]
        for category in spending_vars:
            if category in essential_categories:
                min_amount = expense_dict[category] * 1 # 30% of maximum for essential
                prob += spending_vars[category] >= min_amount
            else:
                min_amount = expense_dict[category] * 0.5  # 10% of maximum for non-essential
                prob += spending_vars[category] >= min_amount
        
        # Solve the problem
        status = prob.solve(PULP_CBC_CMD(msg=False))
        
        if status != 1:
            return None
        
        # Get results
        results = {"Savings": value(savings)}
        for category, var in spending_vars.items():
            results[category] = round(value(var), 2)
        
        # Add zero values for categories that weren't included
        for category in expense_dict:
            if category not in results:
                results[category] = 0
                
        return results

def optimal_budget_input():
    st.set_page_config(
        page_title="Optimal Budget Calculator",
        page_icon="💰",
        layout="wide"
    )
    
    st.title("💰 Optimal Budget Calculator")

    st.subheader(f'Welcome {st.session_state.username}')
    
    optimizer = BudgetOptimizer()
    
    # Initialize session state for form validation
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    
    with st.form(key="budget_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                income = st.number_input(
                    "Monthly Income (INR)",
                    min_value=0.0,
                    step=1000.0,
                    help="Enter your total monthly income"
                )
                
                expenses_dict = {}
                for category in optimizer.expense_categories:
                    expenses_dict[category] = st.number_input(
                        f"{category.replace('_', ' ')} (INR)",
                        min_value=0.0,
                        step=100.0,
                        help=f"Enter your maximum {category.lower()} budget"
                    )
            
            except ValueError as e:
                st.error(f"Please enter valid numbers for all fields: {str(e)}")
                return
        
        with col2:
            savings_goal = st.number_input(
                "Minimum Savings Goal (INR)",
                min_value=0.0,
                step=100.0,
                help="Enter your minimum desired savings amount"
            )
            
            min_spendings = st.multiselect(
                'Select areas to minimize spending:',
                optimizer.expense_categories,
                help="Select categories where you want to reduce expenses"
            )
        
        submit_button = st.form_submit_button("Calculate Optimal Budget")
        
        if submit_button:
            st.session_state.form_submitted = True
            
            # Validate total expenses don't exceed income
            total_expenses = sum(expenses_dict.values())
            if total_expenses + savings_goal > income:
                st.error("⚠️ Total expenses and savings goal cannot exceed your income!")
                return
            
            # Calculate optimal budget
            # with st.spinner("Calculating optimal budget..."):
            optimal_budget = optimizer.optimize_budget(
                income, expenses_dict, min_spendings, savings_goal
            )
            st.session_state.optimal_budget = optimal_budget
            st.session_state.income = income
            # st.write(optimal_budget)  
            # st.write(income)
            # st.write(expenses_dict)  
def display_optimal_budget():
    if st.session_state.optimal_budget:
        st.success("✅ Optimal budget calculated successfully!")
        
        # Display results in a nice format
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Budget Breakdown")
            df = pd.DataFrame({
                'Category': st.session_state.optimal_budget.keys(),
                'Amount (INR)': st.session_state.optimal_budget.values()
            })
            st.dataframe(df.style.format({'Amount (INR)': '{:,.2f}'}))
        
        with col2:
            st.subheader("💡 Summary")
            st.metric("Total Income", f"₹{st.session_state.income:,.2f}")
            st.metric("Optimized Savings", f"₹{st.session_state.optimal_budget['Savings']:,.2f}")
            st.metric(
                "Total Expenses",
                f"₹{sum([v for k, v in st.session_state.optimal_budget.items() if k != 'Savings']):,.2f}"
            )
    else:
        st.error("⚠️ Could not find an optimal solution. Please adjust your constraints.")



