"""from email.utils import collapse_rfc2231_value

import streamlit as st

st.title("Chai Taste Poll")

# st.columns() -> Splits the screen horizontally into columns side-by-side.
col1 , col2 = st.columns(2)

with col1:
    st.header("Masala Chai")
    st.image("https://as1.ftcdn.net/v2/jpg/14/06/85/62/1000_F_1406856223_O15WFRYBMVA4fa9TDAeAiXe589SEUg5X.jpg", width=200)
    vote1 = st.button("Vote Masala Chai")

with col2:
    st.header("Adrak Chai")
    st.image("https://t4.ftcdn.net/jpg/20/82/26/25/240_F_2082262509_8aFCztclEfJ9yFP01dDjOQBPmJANdORx.jpg", width= 400)
    vote2 = st.button("Vote Adrak Chai")

if vote1:
    st.success("Thanks for voting Masala Chai")

if vote2:
    st.success("Thanks for voting Adrak Chai")

# st.sidebar() -> Places widgets inside a collapsible side menu.
name = st.sidebar.text_input("Enter Your Name")
tea = st.sidebar.selectbox("Choose your chai", ["Masala","Kesar","Adrak"])

st.write(f"Welcome {name} and your {tea} chai is getting ready")

# st.expander() -> Creates a collapsible accordion panel to hide/show extra details.
with st.expander("Show Chai Making Instructions"):
    st.write(___)

# st.markdown() -> Displays text formatted with Markdown (**bold**, *italics*, lists, links).
st.markdown("### Welcome To Chai App")
st.markdown("> Blockquote")

#st.toast() ->  Displays a temporary pop-up notification at the bottom corner of the screen.
st.toast("Thanks for trying")

Example->

import streamlit as st

# Add items directly to the sidebar
st.sidebar.title("App Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Password Validator", "Settings"])

st.sidebar.write("---")
st.sidebar.caption("App Version 1.0")

# Main Page Content based on selection
st.title(f"Welcome to the {page} Page")


st.metric() -> Display a metric in big bold font, with an optional indicator of how the metric changed.
st.metric(label="Temperature", value="70 °F", delta="1.2 °F")

st.status() -> Insert a status container to display output from long-running tasks.

"""
