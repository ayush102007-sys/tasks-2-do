import streamlit as st

from OTP import user_database

st.title("Login Portal 🔒")
st.caption("Existing User?")


with st.container(border=True):
    ph = st.text_input("Enter Your Mobile Number *",key="login_no")

if ph in user_database:
    st.success("User Logged in")
