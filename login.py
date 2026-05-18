import streamlit as st

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login function
def login():

    st.title("🔐 InventoryIQ Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "admin" and password == "admin123":

            st.session_state.logged_in = True
            st.success("Login Successful")

        else:
            st.error("Invalid Credentials")

# Dashboard access
if not st.session_state.logged_in:

    login()

else:

    st.switch_page("dashboard.py")