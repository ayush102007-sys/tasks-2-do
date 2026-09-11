import streamlit as st
import requests

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="OmniConvert",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# CACHED HELPER FUNCTIONS
# ==========================================
@st.cache_data(ttl=3600)  # Cache results for 1 hour (3600 seconds)
def fetch_live_rate(base: str, target: str):
    """
    Fetches live exchange rates between base and target currency from Frankfurter API.
    Returns the numeric rate if successful, or None if the request fails.
    """
    url = f"https://api.frankfurter.app/latest?from={base}&to={target}"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            rate = data["rates"][target]
            return rate
        else:
            return None
    except requests.exceptions.RequestException:
        return None


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title(" Navigation")
choice = st.sidebar.radio("Choose Page", ["Converter", "Follow Me"])


# ==========================================
# PAGE 1: CONVERTER
# ==========================================
if choice == "Converter":
    st.title("🌐 OmniConvert: Precision Unit & Currency Hub")
    st.caption("Convert physical measurements instantly and track real-time global currency exchange rates.")

    tab1, tab2 = st.tabs(["⚖️ Physical Units", "🔀 Currency Converter"])

    # --------------------------------------
    # TAB 1: PHYSICAL UNITS
    # --------------------------------------
    with tab1:
        st.subheader("⚖️ Physical Quantity Converter")
        option = st.selectbox("Choose Category:", ["Mass", "Temperature", "Length"])

        # MASS CONVERSION
        if option == "Mass":
            unit_list = ["Milligram", "Gram", "Kilogram", "Metric ton", "Pounds", "Ounces"]

            gram_multipliers = {
                "Milligram": 0.001,
                "Gram": 1.0,
                "Kilogram": 1000.0,
                "Metric ton": 1000000.0,
                "Pounds": 453.59237,
                "Ounces": 28.34952
            }

            col1, col2 = st.columns(2, border=True)

            with col1:
                st.header("From:")
                from_unit = st.selectbox("Select source unit:", unit_list, index=0, key="mass_from_unit")
                from_value = st.number_input("Enter value:", min_value=0.0, value=1.0, key="mass_from_val")

            with col2:
                st.header("To:")
                to_unit = st.selectbox("Select target unit:", unit_list, index=2, key="mass_to_unit")

                # Conversion logic
                base_value_in_grams = from_value * gram_multipliers[from_unit]
                output_value = base_value_in_grams / gram_multipliers[to_unit]

                st.subheader("Converted Result:")
                st.success(f"**{from_value} {from_unit}** = **{output_value:.6f} {to_unit}**")

        # TEMPERATURE CONVERSION
        elif option == "Temperature":
            unit_list = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]

            col1, col2 = st.columns(2, border=True)

            with col1:
                st.header("From:")
                from_unit = st.selectbox("Select source unit:", unit_list, index=0, key="temp_from_unit")
                from_value = st.number_input("Enter value:", value=1.0, key="temp_from_val")

                # Step 1: Normalize to Celsius
                if from_unit == "Celsius (°C)":
                    base_value_in_celsius = from_value
                elif from_unit == "Fahrenheit (°F)":
                    base_value_in_celsius = ((from_value - 32) * 5) / 9
                elif from_unit == "Kelvin (K)":
                    base_value_in_celsius = from_value - 273.15

            with col2:
                st.header("To:")
                to_unit = st.selectbox("Select target unit:", unit_list, index=1, key="temp_to_unit")

                # Step 2: Absolute Zero Validation (-273.15°C)
                if base_value_in_celsius < -273.15:
                    st.error("⚠️ Input temperature is below absolute zero (-273.15°C / -459.67°F / 0K)!")
                else:
                    # Step 3: Convert from Celsius to Target Unit
                    if to_unit == "Celsius (°C)":
                        output_value = base_value_in_celsius
                    elif to_unit == "Fahrenheit (°F)":
                        output_value = ((base_value_in_celsius * 9) / 5) + 32
                    elif to_unit == "Kelvin (K)":
                        output_value = base_value_in_celsius + 273.15

                    st.subheader("Converted Result:")
                    st.success(f"**{from_value} {from_unit}** = **{output_value:.2f} {to_unit}**")

        # LENGTH CONVERSION
        else:  # Option == "Length"
            meter_multipliers = {
                "Millimeters": 0.001,
                "Centimeters": 0.01,
                "Meters": 1.0,
                "Kilometers": 1000.0,
                "Inches": 0.0254,
                "Feet": 0.3048,
                "Yard": 0.9144,
                "Miles": 1609.344
            }

            metric_units = ["Millimeters", "Centimeters", "Meters", "Kilometers"]
            imperial_units = ["Inches", "Yard", "Feet", "Miles"]

            col1, col2 = st.columns(2, border=True)

            with col1:
                st.header("From:")
                unit_type_from = st.selectbox("Select unit system:", ["Metric", "Imperial"], key="from_unit_type")
                from_options = metric_units if unit_type_from == "Metric" else imperial_units
                from_unit = st.selectbox("Select source unit:", from_options, index=0, key="len_from_unit")
                from_value = st.number_input("Enter value:", min_value=0.0, value=1.0, key="len_from_val")

            with col2:
                st.header("To:")
                unit_type_to = st.selectbox("Select unit system:", ["Metric", "Imperial"], key="to_unit_type")
                to_options = metric_units if unit_type_to == "Metric" else imperial_units
                to_unit = st.selectbox("Select target unit:", to_options, index=1, key="len_to_unit")

                # Conversion logic
                base_value_in_meters = from_value * meter_multipliers[from_unit]
                output_value = base_value_in_meters / meter_multipliers[to_unit]

                st.subheader("Converted Result:")
                st.success(f"**{from_value} {from_unit}** = **{output_value:.4f} {to_unit}**")

    # --------------------------------------
    # TAB 2: LIVE CURRENCY
    # --------------------------------------
    with tab2:
        st.subheader("🔀 Live Foreign Exchange Rates")

        currency_list = ["USD", "EUR", "INR", "GBP", "JPY", "CAD", "AUD", "CHF"]

        col1, col2 = st.columns(2, border=True)

        with col1:
            st.header("From:")
            base_curr = st.selectbox("Select Base Currency:", currency_list, index=0, key="curr_base")
            amount = st.number_input("Enter Amount:", min_value=0.01, value=1.0, key="curr_amount")

        with col2:
            st.header("To:")
            target_curr = st.selectbox("Select Target Currency:", currency_list, index=2, key="curr_target")

            if base_curr == target_curr:
                st.warning("⚠️ Please select two different currencies for conversion.")
            else:
                rate = fetch_live_rate(base_curr, target_curr)

                if rate is not None:
                    converted_amount = amount * rate
                    inverse_rate = 1 / rate

                    st.subheader("Converted Result:")
                    st.success(f"**{amount:.2f} {base_curr}** = **{converted_amount:.2f} {target_curr}**")

                    st.divider()
                    m1, m2 = st.columns(2)
                    m1.metric(f"1 {base_curr} =", f"{rate:.4f} {target_curr}")
                    m2.metric(f"1 {target_curr} =", f"{inverse_rate:.4f} {base_curr}")
                else:
                    st.error("❌ Unable to fetch exchange rates. Please check your internet connection or try again later.")


# ==========================================
# PAGE 2: FOLLOW ME / PORTFOLIO LINKS
# ==========================================
else:
    st.title("👨‍💻 Connect with Me")
    st.write("Thanks for checking out **OmniConvert**! Feel free to connect with me on GitHub and LinkedIn.")

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