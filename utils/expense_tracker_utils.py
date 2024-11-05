import streamlit as st
from utils.optimal_budget_utils import BudgetOptimizer
from database.db_config import get_connection
import datetime
import pandas as pd

# date = datetime.date.today()
email = st.session_state.email

def track_expenses_input():
    # date = st.date_input(label="Date")
    optimizer = BudgetOptimizer()
    with st.form(key="budget_form"):
            # col1, col2 = st.columns(2)
        try:
            expenses_dict = {}
            for category in optimizer.expense_categories:
                expenses_dict[category] = st.number_input(
                    f"{category.replace('_', ' ')} (INR)",
                    min_value=0.0,
                    step=100.0,
                    help=f"Enter your maximum {category.lower()} budget"
                )
            submit = st.form_submit_button("Submit")
            if submit:
                # st.success("Tracked to the database")
                budget_data = expenses_dict
                return budget_data
        except ValueError as e:
            st.error(f"Please enter valid numbers for all fields: {str(e)}")


def load_tracked_expenses(date):
    conn = get_connection()
    cursor = conn.cursor(buffered=True)
    query = "SELECT rent,groceries,shopping,daily_spending,loan,bills,other_expenses FROM tracker WHERE email = %s AND tracked_date = %s"
    cursor.execute(query,(email,date))
    values = cursor.fetchone()
    return values

def insert_tracked_expenses(date):
    conn = get_connection()
    cursor = conn.cursor(buffered= True)
    # income = st.session_state.income
    tracked_expenses = st.session_state.tracked_expenses
    rent = tracked_expenses["Rent"]
    groceries = tracked_expenses["Groceries"]
    shopping = tracked_expenses["Shopping"]
    daily_spending = tracked_expenses["Daily_spending"]
    loan = tracked_expenses["Loan"]
    bills = tracked_expenses["Bills"]
    other_expenses = tracked_expenses["Others"]
    query = "INSERT INTO tracker (email, tracked_date,rent,groceries,shopping,daily_spending,loan,bills,other_expenses) VALUES (%s,%s,%s,%s,%s,%s ,%s, %s, %s)"
    cursor.execute(query,(email,date,rent,groceries,shopping,daily_spending,loan,bills,other_expenses))
    conn.commit()
    cursor.close()
    conn.close()

def display_tracked_expense():
    if st.session_state.tracked_expenses:
        st.subheader("📊 Today's tracked expense")
        df = pd.DataFrame({
            'Category': st.session_state.tracked_expenses.keys(),
            'Amount (INR)': st.session_state.tracked_expenses.values()
        })
        st.dataframe(df.style.format({'Amount (INR)': '{:,.2f}'}))
        

def update_tracked_expenses(date):
    conn = get_connection()
    cursor = conn.cursor(buffered= True)
    # income = st.session_state.income
    tracked_expenses = st.session_state.tracked_expenses
    rent = tracked_expenses["Rent"]
    groceries = tracked_expenses["Groceries"]
    shopping = tracked_expenses["Shopping"]
    daily_spending = tracked_expenses["Daily_spending"]
    loan = tracked_expenses["Loan"]
    bills = tracked_expenses["Bills"]
    other_expenses = tracked_expenses["Others"]
    query = "UPDATE tracker SET rent  = %s,groceries =  %s,shopping= %s,daily_spending= %s,loan = %s,bills= %s,other_expenses= %s WHERE email = %s AND tracked_date = %s"
    cursor.execute(query,(rent,groceries,shopping,daily_spending,loan,bills,other_expenses,email,date))
    conn.commit()
    cursor.close()
    conn.close()
    