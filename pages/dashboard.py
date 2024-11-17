import streamlit as st
import numpy as np
import pandas as pd
from database.db_config import get_connection 
import datetime
import plotly.express as px
from utils.rag_utils import prompt_template_dash,get_gemini_response

if "logged_in" in st.session_state and st.session_state.logged_in: 
    if 'optimal_budget' and 'tracked_expenses' in st.session_state:   
        optimal_budget = st.session_state.optimal_budget
        username = st.session_state.username
        tracked_expenses_perday = st.session_state.tracked_expenses
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month

        st.header(f"Monthly Budget Dashboard - {month}/{year}")

        def calculate_cumsum():
            query = f'''select sum(rent),sum(groceries),sum(shopping),sum(daily_spending),sum(loan),sum(bills),sum(other_expenses),year(tracked_date),month(tracked_date) from tracker 
            WHERE email = '{st.session_state.email}' group by 
            year(tracked_date),month(tracked_date) order by year(tracked_date),month(tracked_date)'''
            conn = get_connection()
            cursor = conn.cursor(buffered=True)
            cursor.execute(query)
            data = cursor.fetchall()
            return data
        data = calculate_cumsum()[0]
        expense_cols = columns = [ "Rent", "Groceries", "Shopping", "Daily_spending","Loan", "Bills", "Others"]
        cumulative_expenses = {}
        for expense in range(len(expense_cols)):
            cumulative_expenses[expense_cols[expense]] = data[expense]

        st.session_state.cumulative_expenses = cumulative_expenses

        # Calculations
        categories = [cat for cat in optimal_budget.keys() if cat != "Savings"]
        total_optimal_budget = sum(optimal_budget[cat] for cat in categories)
        total_cumulative_expense = sum(cumulative_expenses[cat] for cat in categories)
        remaining_budget = total_optimal_budget - total_cumulative_expense

        # Dashboard Layout

        # Summary Metrics
        col1,col2 =  st.columns(2)
        with col1:
            st.metric("Total Optimal Budget (Excluding Savings)", f"₹{total_optimal_budget}")
            st.metric("Cumulative Expense to Date", f"₹{total_cumulative_expense}")
        with col2:
            # Additional Savings Display
            # st.write("### Savings Goal")
            st.metric("Optimal Savings for the Month", f"₹{optimal_budget['Savings']}")
            st.metric("Remaining Budget (Excluding Savings)", f"₹{remaining_budget}")

        # Budget vs Actuals Breakdown Table
        data = {
            "Category": categories,
            "Optimal Budget": [optimal_budget[cat] for cat in categories],
            "Cumulative Expense": [cumulative_expenses.get(cat, 0) for cat in categories],
            "Tracked Expense (Today)": [tracked_expenses_perday.get(cat, 0) for cat in categories],
            "Remaining Budget": [optimal_budget[cat] - cumulative_expenses.get(cat, 0) for cat in categories]
        }
        df = pd.DataFrame(data)
        st.write("### Budget vs. Actuals (Excluding Savings)")
        st.dataframe(df)

        # Category-wise Spending Progress Bars
        st.write("### Spending Progress by Category")
        for cat in categories:
            # spent_percentage = cumulative_expenses.get(cat, 0) / optimal_budget[cat] if optimal_budget[cat] or cumulative_expenses.get(cat, 0)<optimal_budget[cat] else 0
            if optimal_budget[cat]:
                if cumulative_expenses.get(cat, 0)<optimal_budget[cat]:
                    spent_percentage = cumulative_expenses.get(cat, 0) / optimal_budget[cat]
                else:
                    spent_percentage = 1.00
            else:
                spent_percentage = 0
            st.progress(spent_percentage, text=f"{cat} ({spent_percentage * 100:.1f}%)")

        # Expense Tracking Over Time (Sample Data)
        # Assuming we have a time series up to today's date
        time_data = pd.DataFrame({
            "Date": pd.date_range(start=f"{year}-{month:02d}-01", end=f"{year}-{month:02d}-04"),
            "Cumulative Expense": [3000, 7200, 9800, total_cumulative_expense]
        })
        fig_time_series = px.line(time_data, x="Date", y="Cumulative Expense", title="Expense Tracking Over Time")
        st.plotly_chart(fig_time_series)

        # Pie Chart of Budget Allocation (Excluding Savings)
        fig_pie = px.pie(names=categories, values=[optimal_budget[cat] for cat in categories], title="Budget Allocation by Category")
        st.plotly_chart(fig_pie)

        # Alerts/Notifications
        st.write("### Alerts")
        for cat in categories:
            if cumulative_expenses.get(cat, 0) > 0.8 * optimal_budget[cat]:
                st.warning(f"⚠️ High spending alert for {cat}: {cumulative_expenses[cat]} / {optimal_budget[cat]} (80% or more of budget)")

        # st.bar_chart(data = cumulative_expenses,x_label="Expense Category",y_label="Amout spend")
        fig = px.bar(x = cumulative_expenses.keys(),y=cumulative_expenses.values(),title="Cumulative Expense in each category")
        st.plotly_chart(fig)

        if st.button("Get AI Report"):
            user_persona = user_data = f"""Username {st.session_state.username} 
            User's todays Spendings {st.session_state.tracked_expenses} 
            User's budget for this month {st.session_state.optimal_budget.items()}
            User's Cumulative expenses: {st.session_state.cumulative_expenses}
            """
            prompt = prompt_template_dash()+user_persona
            response = get_gemini_response(prompt)
            # st.session_state.tracker_res = response
            st.markdown(response)



    else:
        st.warning('Please go to optimal budget page and track your expenses for the day and visit this dashboard')
        st.stop()


else:
    st.warning("Please log in to access this page")
    st.stop()
