import streamlit as st
import pandas as pd
import joblib
import datetime as dt

model = joblib.load("house_price_model (5).pkl")
cols = joblib.load('model_columns (2).pkl')

st.title("House Price Prediction")

col1, col2 = st.columns(2)


with col1:
    size = st.number_input("Size (sq ft)", min_value=500)
    bedrooms = st.number_input("Bedrooms", min_value=1)
    ptype = st.selectbox("Property Type", ["Single Family", "Condominium", "Townhouse"])
with col2:
    sold_date = st.date_input(
    "Sold Date",
    value=dt.date(2024, 1, 1),
    min_value=dt.date(1800, 1, 1),
    max_value=dt.date(2026, 12, 31)
)

    location = st.selectbox("Location", ["CityA", "CityB", "CityC", "CityD"])
    condition = st.selectbox("Condition", ["Poor", "Fair", "Good", "New"])
  



condition_map = {"Poor": 0, "Fair": 1, "Good": 2, "New": 3}


input_dict = {
    "Size": size,
    "Bedrooms": bedrooms,
    "Year_sold": sold_date.year,  
    "month_sold": sold_date.month,    
    "Condition_encoded": condition_map[condition]
}


for t in ["Single Family", "Condominium", "Townhouse"]:
    input_dict[f"Type_{t}"] = 1 if ptype == t else 0

for city in ["CityA", "CityB", "CityC", "CityD"]:
    input_dict[f"Location_{city}"] = 1 if location == city else 0

input_df = pd.DataFrame([input_dict])


for col in cols:
    if col not in input_df.columns:
        input_df[col] = 0

input_df = input_df[cols]

if st.button("Predict Price"):
    prediction = model.predict(input_df)[0]
    st.success(f"### Estimated House Price: ₹ {prediction:,.2f}")