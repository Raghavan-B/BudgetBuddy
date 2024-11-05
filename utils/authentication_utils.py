import streamlit as st
import bcrypt
from database.db_config import get_connection

def login_user_info(email):
    conn = get_connection()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT user_id, name, password_hash FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    if user:
        hashed_pass = user[2].encode("utf-8")
        return user[0], user[1], hashed_pass
    else:
        return None, None, None

def register_user_info(name, email, password):
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    conn = get_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("INSERT INTO users (name, email, password_hash, last_login) VALUES (%s, %s, %s, CURRENT_TIMESTAMP())", (name, email, password_hash))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def register():
    with st.form("register_form"):
        st.header("🔒 Register")
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        button = st.form_submit_button("Register")
        if password != confirm_password:
            st.error("Passwords do not match. 🔑")
        elif button:
            if register_user_info(name, email, password):
                st.session_state.username = name
                st.session_state.email = email
                st.session_state.logged_in = True
                st.success("Registered successfully!")
                st.rerun()
            else:
                st.error("Error registering user. Please try again. 😞")

def login():
    with st.form("login_form"):
        st.header("🔑Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            user_id, name, hashed_pass = login_user_info(email)
            if user_id and bcrypt.checkpw(password.encode("utf-8"), hashed_pass):
                st.session_state.username = name
                st.session_state.email = email
                st.session_state.logged_in = True
                st.success("Logged in successfully!  🎉")
                conn = get_connection()
                cursor = conn.cursor(buffered=True)
                cursor.execute(f"UPDATE users SET last_login = CURRENT_TIMESTAMP() WHERE user_id = {user_id}")
                conn.commit()
                cursor.close()
                conn.close()
                st.rerun()
            else:
                st.error("Invalid Email or Password")
