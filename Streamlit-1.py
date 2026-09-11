import Stream as st          #import command for Streamlit

# st.title() ->  Displays a large main heading for your app.
st.title("Your Favourite Programming Language")

# st.subheader() -> Displays a smaller subsection header.
st.subheader("Designed by streamlit")

# st.text() -> to display raw, preformatted, fixed-width text
st.text("Welcome To My First Interactive App")

# st.write() -> The Swiss Army Knife: Renders almost anything—text, numbers, dictionaries, DataFrames, or charts. Automatically detects the data type.
st.write("Welcome to my first Streamlit web app!")

# st.selectbox() -> Dropdown menu allowing selection of a single item from a list.

program_no = st.selectbox("Choose your password: ", ["C","C++","Python","Java"])
st.write(f"Your choice : {program_no}. Excellent choice")

# st.success() -> Displays a green alert message for successful operations.
st.success(f"Your choice [{program_no}] has been selected")

