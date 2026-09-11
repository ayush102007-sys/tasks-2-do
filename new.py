# To-Do List App
from datetime import date, timedelta
import streamlit as st
from supabase import create_client, Client

st.set_page_config(page_title="Tasks-2-Do", page_icon="⏳")

# Fetch secrets.toml features
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# Track logged-in user
if "user" not in st.session_state:
    st.session_state.user = None

# Initialize tasks structure
if "tasks" not in st.session_state:
    st.session_state.tasks = {"Today": [], "Tomorrow": [], "Next 7 Days": []}

if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = {
        "Today_Complete": [],
        "Tomorrow_Complete": [],
        "Next 7 Days_Complete": [],
    }

if "trashed_tasks" not in st.session_state:
    st.session_state.trashed_tasks = {
        "Today_Trash": [],
        "Tomorrow_Trash": [],
        "Next 7 Days_Trash": [],
    }

if "page" not in st.session_state:
    st.session_state.page = "main"

if "show_success" not in st.session_state:
    st.session_state.show_success = False

# ---------------- AUTHENTICATION GATE ----------------
if st.session_state.user is None:
    st.title("🔒 Welcome to Authentication")
    st.caption("Get started with Tasks-2-Do")

    tab_login, tab_signup = st.tabs(["Log In 🔑", "Sign Up 🆕"])

    # --- LOG-IN TAB ---
    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="abc@gmail.com")
            password = st.text_input("Password", type="password", max_chars=15)
            login_submitted = st.form_submit_button("Log In")

            if login_submitted:
                try:
                    response = supabase.auth.sign_in_with_password(
                        {"email": email, "password": password}
                    )
                    st.session_state.user = response.user
                    st.success("Logged in successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")

    # --- SIGN-UP TAB ---
    with tab_signup:
        with st.form("signup_form"):
            new_email = st.text_input("New Email", placeholder="abc@gmail.com")
            new_password = st.text_input("New password", type="password",max_chars=15)
            signup_submitted = st.form_submit_button("Sign Up")

            if signup_submitted:
                if not new_email or not new_password:
                    st.error("Please enter both an email and password.")
                else:
                    try:
                        response = supabase.auth.sign_up(
                            credentials={
                                "email": new_email.strip(),
                                "password": new_password.strip(),
                            }
                        )
                        st.success(
                            "Account created! Please check your email to confirm or log in."
                        )
                    except Exception as e:
                        st.error(f"Sign Up failed: {e}")
    st.stop()


def load_user_tasks():
    """Fetch tasks belonging strictly to the logged-in user."""
    user_id = st.session_state.user.id

    # Query database for current user's rows
    response = (
        supabase.table("tasks").select("*").eq("user_id", user_id).execute()
    )
    records = response.data

    # Reset local state containers
    st.session_state.tasks = {"Today": [], "Tomorrow": [], "Next 7 Days": []}
    st.session_state.completed_tasks = {
        "Today_Complete": [],
        "Tomorrow_Complete": [],
        "Next 7 Days_Complete": [],
    }
    st.session_state.trashed_tasks = {
        "Today_Trash": [],
        "Tomorrow_Trash": [],
        "Next 7 Days_Trash": [],
    }

    # Populate state based on task status column
    for item in records:
        cat = item["category"]
        status = item["status"]

        if status == "active" and cat in st.session_state.tasks:
            st.session_state.tasks[cat].append(item)
        elif status == "completed":
            st.session_state.completed_tasks[f"{cat}_Complete"].append(
                item["description"]
            )
        elif status == "trashed":
            st.session_state.trashed_tasks[f"{cat}_Trash"].append(item)


# Initial load trigger
if "data_loaded" not in st.session_state or not st.session_state.data_loaded:
    load_user_tasks()
    st.session_state.data_loaded = True

# ---------------- SIDEBAR NAVIGATION ----------------
st.sidebar.title("Task Manager")
st.sidebar.write(f"👤 Logged in as: **{st.session_state.user.email}**")

if st.sidebar.button("🚪 Log Out"):
    supabase.auth.sign_out()
    st.session_state.user = None
    if "data_loaded" in st.session_state:
        del st.session_state.data_loaded
    st.rerun()

st.sidebar.divider()

if st.sidebar.button("➕ Add Task"):
    st.session_state.page = "add_task"
elif st.sidebar.button("🗑️ Delete Task"):
    st.session_state.page = "delete_task"

# ---------------- ADD TASK PAGE ----------------
if st.session_state.page == "add_task":
    st.title("Add a New Task")
    dates = st.selectbox(
        "When To Do the Task",
        ["Today", "Tomorrow", "Next 7 Days"],
        index=None,
        placeholder="Select category",
    )

    today_date = date.today()
    task_date = None
    days_count = None

    with st.form("my_form", clear_on_submit=True):
        new_task = st.text_input(
            "Add New Task Here 👇", placeholder="Write Your Task"
        )

        if dates == "Next 7 Days":
            task_date = st.date_input(
                "Select Specific Date",
                value=today_date + timedelta(days=2),
                min_value=today_date,
                max_value=today_date + timedelta(days=7),
            )
            days_count = (task_date - today_date).days

        your_time = st.time_input(
            "Set time for task (*24 Hour Format*)", value=None
        )
        submitted = st.form_submit_button("Add")

        if submitted:
            if not dates:
                st.warning("Please select a date category first!")
            elif new_task.strip():
                try:
                    task_entry = {
                        "user_id": st.session_state.user.id,
                        "description": new_task.strip(),
                        "category": dates,
                        "status": "active",
                        "time": (
                            your_time.strftime("%H:%M") if your_time else "None"
                        ),
                        "date": (
                            task_date.strftime("%a, %b %d")
                            if task_date
                            else None
                        ),
                        "days_count": days_count if task_date else None,
                    }
                    supabase.table("tasks").insert(task_entry).execute()
                except KeyError:
                    st.toast("Please select time first!")
                else:
                    load_user_tasks()
                    st.session_state.show_success = True
                    st.session_state.page = "main"
                    st.rerun()
            else:
                st.warning("Please enter a valid task description.")

    if st.button("Cancel"):
        st.session_state.page = "main"
        st.rerun()

# ---------------- DELETE TASK PAGE ----------------
elif st.session_state.page == "delete_task":
    st.title("Delete Tasks")

    option = st.selectbox(
        "Select Category",
        ["Today", "Tomorrow", "Next 7 Days"],
        index=None,
        placeholder="--Select--",
    )
    if option:
        task_list = st.session_state.tasks[option]
        if not task_list:
            st.info(f"No active tasks in {option}.")
        else:
            with st.container(border=True):
                for added_task in task_list:
                    if st.checkbox(
                        f"🗑️ Delete task: {added_task['description']}",
                        key=f"del_task_{added_task['id']}",
                    ):
                        supabase.table("tasks").update(
                            {"status": "trashed"}
                        ).eq("id", added_task["id"]).execute()
                        st.session_state.show_success = (
                            "Task moved to Trash! 🗑️"
                        )
                        load_user_tasks()
                        st.rerun()

    if st.button("Done / Cancel"):
        st.session_state.page = "main"
        st.rerun()

# ---------------- MAIN PAGE ----------------
elif st.session_state.page == "main":
    st.title("Stay Organized, Stay Creative")
    st.caption("Whether it's work projects, personal tasks, or study plans,"
               " Tasks-2-Do helps you organize and confidently tackle everything in your life.")

    if st.session_state.show_success:
        st.success("Task updated successfully! 🎉")
        st.session_state.show_success = False

    choice = st.sidebar.radio("My Tasks", ["Inbox", "Completed", "Trash", "Follow Creator"])

    if choice == "Inbox":
        with st.container(border=True):
            with st.expander("Today", expanded=True):
                for task in st.session_state.tasks["Today"]:
                    if st.checkbox(
                        f"📝 {task['description']}",
                        key=f"chk_today_{task['id']}",
                    ):
                        supabase.table("tasks").update(
                            {"status": "completed"}
                        ).eq("id", task["id"]).execute()
                        load_user_tasks()
                        st.rerun()
                    st.caption(f"🕒 Time: {task['time']}")

        with st.container(border=True):
            with st.expander("Tomorrow", expanded=True):
                for task in st.session_state.tasks["Tomorrow"]:
                    if st.checkbox(
                        f"📝 {task['description']}",
                        key=f"chk_tomorrow_{task['id']}",
                    ):
                        supabase.table("tasks").update(
                            {"status": "completed"}
                        ).eq("id", task["id"]).execute()
                        load_user_tasks()
                        st.rerun()
                    st.caption(f"🕒 Time: {task['time']}")

        with st.container(border=True):
            with st.expander("Next 7 Days", expanded=True):
                for task in st.session_state.tasks["Next 7 Days"]:
                    if st.checkbox(
                        f"📝 {task['description']}",
                        key=f"chk_next_{task['id']}",
                    ):
                        supabase.table("tasks").update(
                            {"status": "completed"}
                        ).eq("id", task["id"]).execute()
                        load_user_tasks()
                        st.rerun()
                    date_str = (
                        f" | 📅 {task['date']}" if task.get("date") else ""
                    )
                    days_str = (
                        f" | {task['days_count']}d left"
                        if task.get("days_count") is not None
                        else ""
                    )
                    st.caption(f"🕒 Time: {task['time']}{date_str}{days_str}")

    elif choice == "Completed":
        st.subheader("Completed Tasks ✅")
        with st.expander("Today", expanded=True):
            for num, complete_task in enumerate(
                st.session_state.completed_tasks["Today_Complete"]
            ):
                st.write(f"{num+1}. {complete_task}")

        with st.expander("Tomorrow", expanded=True):
            for num, complete_task in enumerate(
                st.session_state.completed_tasks["Tomorrow_Complete"]
            ):
                st.write(f"{num+1}. {complete_task}")

        with st.expander("Next 7 Days", expanded=True):
            for num, complete_task in enumerate(
                st.session_state.completed_tasks["Next 7 Days_Complete"]
            ):
                st.write(f"{num+1}. {complete_task}")

    elif choice == "Trash":
        st.subheader("Trash Bin 🗑️")

        categories = [
            ("Today", "Today_Trash"),
            ("Tomorrow", "Tomorrow_Trash"),
            ("Next 7 Days", "Next 7 Days_Trash"),
        ]

        for cat_name, cat_key in categories:
            with st.expander(cat_name, expanded=True):
                trashed_list = st.session_state.trashed_tasks[cat_key]
                if not trashed_list:
                    st.caption("No trashed tasks here.")
                else:
                    for task in trashed_list:
                        col1, col2 = st.columns([0.75, 0.25])
                        with col1:
                            st.write(f"🗑️ {task['description']}")
                        with col2:
                            if st.button(
                                "♻️ Restore",
                                key=f"res_{task['id']}",
                                use_container_width=True,
                            ):
                                supabase.table("tasks").update(
                                    {"status": "active"}
                                ).eq("id", task["id"]).execute()
                                load_user_tasks()
                                st.toast("Task restored successfully!")
                                st.rerun()

    # ==========================================
    # FOLLOW ME / PORTFOLIO LINKS
    # ==========================================
    else:
        st.title("👨‍💻 Connect with Creator")
        st.write("Thanks for checking out **Tasks-2-Do**! Feel free to connect with me on GitHub and LinkedIn.")

        st.divider()

        col1, col2 = st.columns(2, border=True)

        with col1:
            st.subheader("🐙 GitHub")
            st.write("Explore my code repositories, projects, and contributions.")
            st.link_button("Visit GitHub Profile", "https://github.com/ayush102007-sys")

        with col2:
            st.subheader("💼 LinkedIn")
            st.write("Connect with me professionally and follow my tech journey.")
            st.link_button("Visit LinkedIn Profile", "https://linkedin.com/in/ayush-2007-it")
