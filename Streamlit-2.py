"""import streamlit as st

st.title("Chai Maker App")

if st.button("Make Chai"):      #Returns True when clicked, triggering actions or calculations.
    st.success("Your chai is being brewed")

add_masala = st.checkbox("Add Masala")      #Toggle box returning True or False.

if add_masala:
    st.write("Masala added to your chai")

# st.radio() -> Radio buttons for choosing one option from a visible list.
tea_type = st.radio("Pick your chai base: ", ["Milk","Water","Honey"])
st.write(f"Selected base: {tea_type}")

flavour = st.selectbox("Choose flavour: ", ["Adrak","Kesar","Tulsi"])
st.write(f"Selected flavour: {flavour}")

# st.slider() -> Numeric slider for selecting numbers within a range.
sugar = st.slider("Sugar level", 0, 5, 2)
st.write(f"Sugar Level: {sugar}")

# st.number_input() -> Selecting numbers as input within a range.
cups = st.number_input("How many cups", min_value=1, max_value=10, step=1)
st.write(f"No.of cups selected: {cups}")

# st.text_input() -> Single-line text field (e.g., entering a password or username).
name = st.text_input("Enter your name")
if name:
    st.write(f"Welcome, {name} ! Your chai is on the way :)")

dob = st.date_input("Select your date of birth")
st.write(f"Selected DOB: {dob}")



             if clean_text(user_ans) in ["a", "b", "c", "d"]:
                # Evaluate using helper function
                if evaluate_answer(user_ans, item["answer"]):
                    st.success("✅ Correct!")
                    score += 1
             else:
                st.warning(f"❌ Incorrect! The correct answer was: {item['answer']}")
        else:
            # Note: print() outputs to terminal, not Streamlit app
            st.error("⚠️ Invalid option selected! Question marked incorrect.")

        # Note: print() outputs to terminal, not Streamlit app
        st.sidebar.metric(label="Current Score", value=f"{score}/{total_questions}")



st.radio() -> Why Use the key Parameter?

    for ques_no, item in enumerate(question_bank, 1):
        st.write(f"\nQuestion [{ques_no}/{total_questions}]: {item['question']}")
        st.write("Options:", " | ".join(item["options"]))

        user_ans = st.radio("Options ->", ["A", "B", "C", "D"])

There are multiple radio elements with the same auto-generated ID. 
When this element is created, it is assigned an internal ID based on the element type and provided parameters. 
Multiple elements with the same type and parameters will cause this error.

To fix this error, please pass a unique key argument to the radio element.

import streamlit as st

with st.container(border=True):
    st.write("Security Check")
    st.text_input("Enter password:", type="password")

with st.container(height=150):
    st.write("Log 1: App started")
    st.write("Log 2: User logged in")
    st.write("Log 3: Data processed successfully")
    st.write("Log 4: Session Ended")

"""