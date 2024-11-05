import streamlit as st
import bcrypt
from database.db_config import get_connection
from utils.authentication_utils import login,register

def hello():
    st.header(f"Hello {st.session_state.username} 👋")
    st.write("Welcome to our application!")

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