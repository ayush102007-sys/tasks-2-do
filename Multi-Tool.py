import streamlit as st

st.title("My Multi-Tool App")

# st.tabs()- splits your screen horizontally into clickable tab headers.

tab1, tab2, tab3 = st.tabs(["Home","Calculator","History"])

with tab1:
    st.header("Welcome!")
    st.write("This is the main home section")

with tab2:
    st.header("Age Calculator")
    age = st.number_input("Enter your age:", min_value= 1, max_value= 100)
    st.write(f"You entered: {age}")

with tab3:
    st.header("Preferences")
    st.checkbox("Enable Notifications")



