import streamlit as st
from utils.optimal_budget_utils import BudgetOptimizer
import pandas as pd

def main():
    st.set_page_config(
        page_title="Optimal Budget Calculator",
        page_icon="💰",
        layout="wide"
    )
    
    st.title("💰 Optimal Budget Calculator")
    
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
            with st.spinner("Calculating optimal budget..."):
                optimal_budget = optimizer.optimize_budget(
                    income, expenses_dict, min_spendings, savings_goal
                )
            
            if optimal_budget:
                st.success("✅ Optimal budget calculated successfully!")
                
                # Display results in a nice format
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Budget Breakdown")
                    df = pd.DataFrame({
                        'Category': optimal_budget.keys(),
                        'Amount (INR)': optimal_budget.values()
                    })
                    st.dataframe(df.style.format({'Amount (INR)': '{:,.2f}'}))
                
                with col2:
                    st.subheader("💡 Summary")
                    st.metric("Total Income", f"₹{income:,.2f}")
                    st.metric("Optimized Savings", f"₹{optimal_budget['Savings']:,.2f}")
                    st.metric(
                        "Total Expenses",
                        f"₹{sum([v for k, v in optimal_budget.items() if k != 'Savings']):,.2f}"
                    )
            else:
                st.error("⚠️ Could not find an optimal solution. Please adjust your constraints.")
if __name__ == "__main__":
    main()
    if st.session_state.form_submitted == True:
        # Satisfaction feedback
        satisfaction = st.radio(
            "Are you satisfied with this budget?",
            ["Yes", "No"],
            horizontal=True,
            key="satisfaction",
            index=None
        )
        if satisfaction == "Yes":
            st.write("✅ Optimal budget stored to db successfully!")
        if satisfaction == "No":
            st.info("💡 Tip: Try adjusting your minimum savings goal or selecting different categories to minimize.")
        