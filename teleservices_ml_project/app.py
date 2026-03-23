
import streamlit as st
import pandas as pd
import joblib

# Load model and columns
model = joblib.load("telehealth_demand_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")

st.title("Telehealth Demand Prediction App")

st.write("Enter input details to predict demand")

# Inputs
year = st.number_input("Year", value=2022)
month = st.number_input("Month (YYYYMM)", value=202201)
rate = st.number_input("Rate Per 1000 Beneficiaries", value=1.0)

state = st.selectbox("State", [col.replace("State_", "") for col in feature_columns if "State_" in col])

telehealth_type = st.selectbox(
    "Telehealth Type",
    ["Live audio/video", "Other telehealth", "Remote patient monitoring", "Store and forward"]
)

service_type = st.selectbox("Service Type", ["All"])

# Create input dataframe
input_data = pd.DataFrame([[0]*len(feature_columns)], columns=feature_columns)

input_data["Year"] = year
input_data["Month"] = month
input_data["RatePer1000Beneficiaries"] = rate

# Encode selections
state_col = f"State_{state}"
if state_col in input_data.columns:
    input_data[state_col] = 1

tele_col = f"TelehealthType_{telehealth_type}"
if tele_col in input_data.columns:
    input_data[tele_col] = 1

service_col = f"ServiceType_{service_type}"
if service_col in input_data.columns:
    input_data[service_col] = 1

# Predict
if st.button("Predict"):
    prediction = model.predict(input_data)[0]
    st.success(f"Predicted Demand: {prediction:,.0f}")