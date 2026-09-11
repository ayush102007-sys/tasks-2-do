from datetime import date
import streamlit as st

# MUST BE THE FIRST STREAMLIT COMMAND IN THE SCRIPT
st.set_page_config(page_title="Age Calculator", page_icon="📅")


def calculate_age(total_days, days_in_year=365.25, days_in_month=30.44):
    years = int(total_days // days_in_year)
    remaining_days = total_days % days_in_year

    months = int(remaining_days // days_in_month)
    days = round(remaining_days % days_in_month)

    return years, months, days


def get_zodiac_sign(day, month):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries ♈"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus ♉"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini ♊"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer ♋"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo ♌"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo ♍"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra ♎"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio ♏"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius ♐"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn ♑"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius ♒"
    else:
        return "Pisces ♓"


zodiac_traits = {
    "Aries ♈": "Eager, dynamic, quick, and competitive.",
    "Taurus ♉": "Strong, dependable, sensual, and creative.",
    "Gemini ♊": "Expressive, quick-witted, curious, and adaptable.",
    "Cancer ♋": "Compassionate, emotional, fierce, and intuitive.",
    "Leo ♌": "Dramatic, outgoing, fiery, and self-assured.",
    "Virgo ♍": "Practical, loyal, gentle, and analytical.",
    "Libra ♎": "Social, fair-minded, diplomatic, and gracious.",
    "Scorpio ♏": "Passionate, stubborn, resourceful, and brave.",
    "Sagittarius ♐": "Extraverted, optimistic, funny, and generous.",
    "Capricorn ♑": "Independent, disciplined, tenacious, and fierce.",
    "Aquarius ♒": "Deep, imaginative, original, and uncompromising.",
    "Pisces ♓": "Affectionate, empathetic, wise, and artistic."
}


def get_time_breakdown(total_days):
    total_months = int(total_days / 30.4375)  # Average days in a month
    total_weeks = int(total_days / 7)
    total_hours = total_days * 24
    total_minutes = total_hours * 60
    total_seconds = total_minutes * 60

    return {
        "Months": f"{total_months:,}",
        "Weeks": f"{total_weeks:,}",
        "Days": f"{total_days:,}",
        "Hours": f"{total_hours:,}",
        "Minutes": f"{total_minutes:,}",
        "Seconds": f"{total_seconds:,}",
    }


# Global Ko-fi Username
kofi_username = "codeby_ayush"

# Sidebar Navigation
st.sidebar.title("Website Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Calculator Page", "Support the Creator"])

if page == "Home":
    st.title("📅 Precision Age Calculator")

    st.markdown("""
    **Welcome to the Precision Age Calculator!**  
    Easily compute your exact age down to the exact years, months, and days. 
    Whether you're tracking upcoming birthdays or calculating exact date intervals, get instant, accurate results below.
    """)

    st.write("---")

    with st.expander("ℹ️ How are leap years and months calculated?"):
        st.write(
            "Our algorithm accounts for varying month lengths (28 to 31 days) and leap year cycles to guarantee 100% mathematical accuracy."
        )
    with st.expander("🎉 Fun Stats & Milestones"):
        st.markdown("""
        * **Did you know?** Over a standard lifetime, your heart beats approximately **2.5 billion times**.
        * **Leap Years:** A normal year has 365 days, but leap years add an extra day every 4 years to keep our calendar synchronized with the Earth's orbit around the Sun.
        * **Next Birthday:** Use our tool below to keep track of the exact day of the week your next birthday falls on!
        """)
    with st.expander("⚙️ How the Calculation Works"):
        st.markdown("""
        * **Exact Month Lengths:** Our Python logic calculates the exact number of days in each month (28, 29, 30, or 31) rather than taking a rough 30-day average.
        * **Leap Year Support:** Built using Python's standard `datetime` module to account for February 29th during leap years.
        * **Timezone Safety:** All date calculations rely on midnight boundary comparisons to avoid timezone drift errors.
        """)
    with st.expander("📖 How to Use This Tool"):
        st.markdown("""
        1. **Select Date of Birth:** Click the calendar widget under the input section to pick your birth date.
        2. **Choose Target Date (Optional):** By default, your age is calculated as of today. You can change this to calculate your age on a specific future or past date.
        3. **View Results:** Instantly view your total age broken down into **Years, Months, and Days**.
        """)
    with st.expander("✨ Discover Your Zodiac & Cosmic Stats"):
        st.markdown("""
        * **What's Your Sign?** Depending on your date of birth, your astronomical sun sign determines your unique cosmic archetype and personality traits.
        * **Four Elements:** Every zodiac sign belongs to one of the four natural elements—**Fire** (Energy), **Earth** (Grounding), **Air** (Intellect), or **Water** (Emotion).
        * **Astrological Milestone:** Every 12 years, Jupiter returns to the exact position it was in when you were born, marking a major cycle of personal growth and luck!
        """)

elif page == "Calculator Page":
    with st.container(border=True):
        st.title("Age Calculator")
        st.subheader("Calculate your age in a very simple way")

    today_date = date.today()

    with st.container(border=True):
        dob = st.date_input(
            "Select your Date of Birth",
            value=date(2000, 1, 1),
            min_value=date(1950, 1, 1),
            max_value=today_date,
        )

        st.subheader("Choose calculation method")
        method1, method2 = st.tabs(["Age Today", "At Date"])

        with method1:
            date_today = st.date_input(
                "Today's Date", value=today_date, key="today_m1"
            )

            if dob:
                days_count = (date_today - dob).days
                if days_count < 0:
                    st.error(
                        "Date of Birth cannot be after the selected date!"
                    )
                else:
                    y, m, d = calculate_age(days_count)
                    st.success(f"**Age:** {y} Years, {m} Months, {d} Days")

        with method2:
            selected_date = st.date_input(
                "Select Target Date", value=today_date, key="target_m2"
            )

            if dob:
                days_count = (selected_date - dob).days
                if days_count < 0:
                    st.error(
                        "Date of Birth cannot be after the selected date!"
                    )
                else:
                    y, m, d = calculate_age(days_count)
                    st.success(f"**Age:** {y} Years, {m} Months, {d} Days")

        st.write("---")
        feature = st.checkbox("Turn on advanced features")

        if feature:
            st.toast("Advanced Settings Turned On")
            option = st.selectbox(
                "Select feature:", ["Day you were born", "Next Birthday", "Your Zodiac Sign", "Total Time Lived"]
            )

            if option == "Day you were born":
                st.write(f"You were born on a: **{dob.strftime('%A')}**")

            elif option == "Next Birthday":
                b_month = dob.month
                b_day = dob.day

                try:
                    next_birthday = date(today_date.year, b_month, b_day)
                except ValueError:
                    next_birthday = date(today_date.year, 2, 28)

                if next_birthday < today_date:
                    try:
                        next_birthday = date(today_date.year + 1, b_month, b_day)
                    except ValueError:
                        next_birthday = date(today_date.year + 1, 2, 28)

                days_left = (next_birthday - today_date).days

                st.divider()
                if days_left == 0:
                    st.balloons()
                    st.success("🎉 Happy Birthday! It's happening today!")
                else:
                    st.metric(
                        label="Days Remaining until Birthday",
                        value=f"{days_left} days",
                    )
                    st.info(
                        f"Your next birthday falls on a **{next_birthday.strftime('%A, %B %d, %Y')}**."
                    )

            elif option == "Your Zodiac Sign":
                if dob:
                    birth_day = dob.day
                    birth_month = dob.month
                    sign = get_zodiac_sign(birth_day, birth_month)

                    st.metric(label="Your Zodiac Sign", value=sign)
                    st.info(f"**Personality Traits:** {zodiac_traits[sign]}")

            elif option == "Total Time Lived":
                days_lived = (today_date - dob).days

                if days_lived < 0:
                    st.error("Date of birth cannot be in the future!")
                else:
                    stats = get_time_breakdown(days_lived)

                    st.subheader("⏱️ Total Time Breakdown")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Months", stats["Months"])
                        st.metric("Total Hours", stats["Hours"])

                    with col2:
                        st.metric("Total Weeks", stats["Weeks"])
                        st.metric("Total Minutes", stats["Minutes"])

                    with col3:
                        st.metric("Total Days", stats["Days"])
                        st.metric("Total Seconds", stats["Seconds"])

elif page == "Support the Creator":
    st.title("☕ Support the Creator")
    st.write("Thanks for using Precision Age Calculator! If this tool saved you time or was helpful, feel free to buy me a coffee.")

    kofi_badge_html = f"""
    <div style="text-align: center; margin-top: 30px;">
        <a href='https://ko-fi.com/{kofi_username}' target='_blank'>
            <img height='45' style='border:0px;height:45px;' 
                 src='https://storage.ko-fi.com/cdn/kofi3.png?v=3' 
                 border='0' 
                 alt='Buy Me a Coffee at ko-fi.com' />
        </a>
    </div>
    """
    st.markdown(kofi_badge_html, unsafe_allow_html=True)


