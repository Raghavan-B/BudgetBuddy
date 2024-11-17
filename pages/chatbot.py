import streamlit as st
from utils.rag_utils import format_docs
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from utils.rag_utils import format_docs,prompt_template_chat,load_vectorstore_as_retriever

if "logged_in" in st.session_state and st.session_state.logged_in: 
    if 'optimal_budget' and 'tracked_expenses' and 'cumulative_expenses' in st.session_state:   
        ## Do the chatbot interface
        ## Streamlit chatbot input
        ## Load the vector db
        ## Finally do similarity search and return the responses
        optimal_budget = st.session_state.optimal_budget
        tracked_expenses = st.session_state.tracked_expenses
        cumulative_expenese = st.session_state.cumulative_expenses

        user_data = f"""Username {st.session_state.username} User's todays Spendings {tracked_expenses.items()} User's budget for this month {optimal_budget.items()} User's 
                        User's cumulative expense list for each category for this month {cumulative_expenese.items()} """
        retriever = load_vectorstore_as_retriever()
        template = prompt_template_chat()+user_data

        prompt = ChatPromptTemplate.from_template(template)
        model = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash')


        chain = (
            {"context": retriever | format_docs,"question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )

        st.header("Welcome to Our Finance Expert Chatbot!!")
        query = st.chat_input(placeholder="Enter your query: ")
        if query:
            st.write(f"Question {query}")
            response = chain.invoke(query)
            st.markdown(f"Bot Response: \n {response}")


    else:
        st.warning('Please go to optimal budget page and track your expenses for the day and visit the dashboard first')
        st.stop()




else:
    st.warning("This feature still in progress")
    st.stop()