import streamlit as st
import pandas as pd
# from utils.optimal_budget_utils import optimal_budget_input,display_optimal_budget
from database.db_config import get_connection
import datetime


date = datetime.date.today()
month = datetime.datetime.now().month
year = datetime.datetime.now().year
columns = [ "Income","Savings","Rent", "Groceries", "Shopping", "Daily_spending","Loan", "Bills", "Others"]



if "logged_in" in st.session_state and st.session_state.logged_in:    
    from utils.optimal_budget_utils import load_optimal_budget,insert_optimal_budget,optimal_budget_input,display_optimal_budget
    # email = st.session_state.email
    if load_optimal_budget() is None:
        optimal_budget_input()
        if st.session_state.form_submitted == True:
            # Satisfaction feedback
            display_optimal_budget()
            satisfaction = st.radio(
                "Are you satisfied with this budget?",
                ["Yes", "No"],
                horizontal=True,
                key="satisfaction",
                index=None
            )
            if satisfaction == "Yes":
                insert_optimal_budget()
                st.write("✅ Optimal budget stored to db successfully!")
                st.rerun()
            if satisfaction == "No":
                st.info("💡 Tip: Try adjusting your minimum savings goal or selecting different categories to minimize.")
    else:
        values = load_optimal_budget()
        income = values[0]
        optimal_budget = {}
        for i in range(1,len(columns)):
            optimal_budget[columns[i]] = values[i]
        st.session_state.optimal_budget = optimal_budget
        st.session_state.income = income
        display_optimal_budget()
else:
    st.warning("Please log in to access this page")
    st.stop()


        