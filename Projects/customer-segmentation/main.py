from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "kmeans_model.pkl"
SCALER_PATH = PROJECT_DIR / "scaler.pkl"

FEATURES = [
    "Age",
    "Income",
    "NumWebPurchases",
    "NumStorePurchases",
    "NumWebVisitsMonth",
    "Total_spend",
]

st.set_page_config(page_title="Customer Segmentation", page_icon="📊")
st.title("Customer Segmentation")
st.write("Enter customer details to predict the customer's K-Means segment.")

@st.cache_resource
def load_artifacts():
    if not MODEL_PATH.is_file() or not SCALER_PATH.is_file():
        raise FileNotFoundError(
            "Model artifacts are missing. Keep kmeans_model.pkl and scaler.pkl "
            "in the same folder as main.py."
        )
    return joblib.load(MODEL_PATH), joblib.load(SCALER_PATH)

try:
    kmeans, scaler = load_artifacts()
except Exception as exc:
    st.error(f"Could not load the trained model: {exc}")
    st.stop()

with st.form("customer_details"):
    age = st.number_input("Age", min_value=5, max_value=130, value=18)
    income = st.number_input(
        "Annual income", min_value=0, max_value=1_500_098, value=80_000
    )
    total_spend = st.number_input(
        "Total spend across products", min_value=0, max_value=9_999_999, value=1_000
    )
    web_purchases = st.number_input(
        "Online purchases", min_value=0, max_value=31, value=7
    )
    store_purchases = st.number_input(
        "In-store purchases", min_value=0, max_value=31, value=7
    )
    web_visits = st.number_input(
        "Website visits per month", min_value=0, max_value=31, value=7
    )
    submitted = st.form_submit_button("Predict segment")

if submitted:
    customer = pd.DataFrame(
        [[age, income, web_purchases, store_purchases, web_visits, total_spend]],
        columns=FEATURES,
    )
    try:
        scaled_customer = scaler.transform(customer)
        cluster = int(kmeans.predict(scaled_customer)[0])
        st.success(f"Predicted customer cluster: {cluster}")
        st.caption(
            "Cluster IDs identify groups learned by K-Means; they do not imply "
            "an ordinal ranking."
        )
    except Exception as exc:
        st.error(f"Prediction failed: {exc}")
