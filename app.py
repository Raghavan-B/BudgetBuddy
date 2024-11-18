import streamlit as st
import bcrypt
from database.db_config import get_connection
from utils.authentication_utils import login,register

def hello():
    st.title("Welcome to BudgetBuddy!")
    st.subheader("Your Personal Finance Optimization Partner")

    st.header(f"Hello {st.session_state.username} 👋")
    st.markdown("""
        ### What is BudgetBuddy?
        BudgetBuddy is a personal finance management app that helps you:
        - Allocate optimal budgets for your monthly expenses.
        - Track your daily expenses.
        - Monitor your progress towards achieving monthly savings goals.
        - Get personalized financial recommendations via a chatbot.
        
        ### How to Use the App
        Follow these steps to make the most of BudgetBuddy:
        1. **Optimal Budget Page**: Calculate your monthly budget allocation using optimization techniques.
        2. **Tracker Page**: Track your daily expenses in categories such as Rent, Groceries, etc.
        3. **Dashboard Page**: Visualize your spending trends and compare them with your optimal budget.
        4. **Chatbot Page**: Ask any financial questions and get personalized advice based on your spending habits.
    """)

def main():
    st.set_page_config(page_title="Login and Registration")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if st.session_state.logged_in:
        hello()
    else:
        pages = {
            "Login": login,
            "Register": register
        }
        selection = st.sidebar.radio("Select a page", list(pages.keys()))
        pages[selection]()

if __name__ == "__main__":
    main()