import streamlit as st
import random

st.set_page_config(
    page_title= "Login",
    page_icon= "🔐"
)

user_database = []

if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None

st.title("Sign up Portal 🔒")
st.caption("New User?")
with st.container(border= True):
    ph = st.text_input("Enter Your Mobile Number *",key="signup_no", max_chars= 10)
    user_database.append(ph)

    if ph and len(ph) == 10:
        if st.button("Send OTP"):
            otp = ""
            for i in range(6):
                new_otp = str(random.randint(0,9))
                otp += new_otp
                st.session_state.generated_otp = otp
            st.toast(f"Your OTP is {otp}", duration= 20)

            # 3. Verify OTP input
        if st.session_state.generated_otp:
            give_otp = st.text_input("Enter OTP", max_chars=6)

            if len(give_otp) == 6:
                if give_otp == st.session_state.generated_otp:
                    st.success("✅ Phone number verified!")
                else:
                    st.error("❌ Invalid OTP")

    st.page_link("pages/login.py", label="Already Have an Account?")

