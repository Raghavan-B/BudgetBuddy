import streamlit as st
import datetime 
## this page will track day to day expenses for each day
if "logged_in" in st.session_state and st.session_state.logged_in:
    # from utils.optimal_budget_utils import BudgetOptimizer
    from utils.expense_tracker_utils import update_tracked_expenses,track_expenses_input,load_tracked_expenses,insert_tracked_expenses,display_tracked_expense
    columns = ["Rent", "Groceries", "Shopping", "Daily_spending","Loan", "Bills", "Others"]
    st.title(f"Welcome to tracker, {st.session_state.username}!!")
    # expenses = track_expenses_input()
    date = st.date_input("Date: ")
    if load_tracked_expenses(date) is None:
        budget_data = track_expenses_input()
        st.session_state.tracked_expenses = budget_data 

        if budget_data:
            insert_tracked_expenses(date)
            st.success("Tracked your expenses !!")
            st.rerun()
    else:
        values = load_tracked_expenses(date)
        tracked_expenses = {}
        for i in range(0,len(columns)):
            tracked_expenses[columns[i]] = values[i]
        st.session_state.tracked_expenses = tracked_expenses
        # st.session_state.income = income
        display_tracked_expense()
        update = st.radio("Do you want to update your tracking?? :",options=["Yes","No"],horizontal=True,index=None)
        if update == "Yes":
            st.write("OK!!")
            update_expenses = track_expenses_input()
            if update_expenses:
                for i in tracked_expenses:
                    tracked_expenses[i]+=update_expenses[i]
                    st.session_state.tracked_expenses = tracked_expenses
                    ##Update function to database:
                    update_tracked_expenses(date)

else:
    st.warning("Please log in to access this page")
    st.stop()
