import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import os
import urllib.request
st.set_page_config(layout="wide", page_title="Crowd-Flow Fairness")
st.title("🧭 Crowd-Flow Fairness Predictor")
st.write("Predict hourly footfall and get the best visiting time recommendations.")
MODEL_URL = "https://github.com/DarshiniSivakumar/CROWD_FLOW_FAIRNESS_PROJECT/raw/main/crowd_model.pkl"
PREPROC_URL = "https://github.com/DarshiniSivakumar/CROWD_FLOW_FAIRNESS_PROJECT/raw/main/preprocessor.pkl"
if not os.path.exists("crowd_model.pkl"):
    urllib.request.urlretrieve(MODEL_URL, "crowd_model.pkl")
if not os.path.exists("preprocessor.pkl"):
    urllib.request.urlretrieve(PREPROC_URL, "preprocessor.pkl")
model = joblib.load("crowd_model.pkl")
preproc = joblib.load("preprocessor.pkl")
le_place = preproc["le_place"]
le_city = preproc["le_city"]
FEATURES = preproc["features"]
tn_cities = [
    "Chennai","Coimbatore","Madurai","Tiruchirappalli","Salem","Erode","Tirunelveli",
    "Vellore","Tiruppur","Thoothukudi","Karur","Nagercoil","Cuddalore","Dindigul",
    "Kanchipuram","Kanyakumari","Sivakasi","Pollachi","Ramanathapuram","Villupuram"
]
with st.sidebar:
    st.header("Input Conditions")
    place_type = st.selectbox("Place type", sorted(list(le_place.classes_)))
    city_choice = st.selectbox("City (TN)", tn_cities + ["Other / Custom"])
    if city_choice == "Other / Custom":
        city_custom = st.text_input("Enter city/town name", "")
        city = city_custom.strip()
    else:
        city = city_choice
    location = st.text_input("Location / area (optional)", value="")
    temp = st.number_input("Temperature (°C)", value=30.0, step=0.5)
    rain = st.number_input("Rain in last hour (mm)", value=0.0, step=0.1)
    clouds = st.slider("Cloud coverage (%)", 0, 100, 40)
    event_density = st.slider("Event density (0 none - 1 heavy)", 0.0, 1.0, 0.0, 0.1)
    date = st.date_input("Date", datetime.today())
    hour = st.slider("Hour (0–23)", 0, 23, datetime.now().hour)
if not city:
    st.sidebar.error("Please enter or select a city.")
    st.stop()
day = date.day
month = date.month
dayofweek = date.weekday()
def safe_transform_label(le, val):
    try:
        return int(le.transform([val])[0])
    except Exception:
        return 0  # unseen labels default to 0
place_code = safe_transform_label(le_place, place_type)
city_code = safe_transform_label(le_city, city)
input_row = pd.DataFrame([{
    "place_code": place_code,
    "city_code": city_code,
    "temp_celsius": temp,
    "rain_1h": rain,
    "clouds_all": clouds,
    "day": day,
    "hour": hour,
    "month": month,
    "dayofweek": dayofweek,
    "event_density": event_density
}])
for col in FEATURES:
    if col not in input_row.columns:
        input_row[col] = 0
st.subheader("Predict Now")
if st.button("Predict Crowd"):
    # Ensure input columns match training features
    missing_cols = [c for c in FEATURES if c not in input_row.columns]
    for c in missing_cols:
        input_row[c] = 0
    base_pred = int(model.predict(input_row[FEATURES])[0])
    adj_factor = 1.0
    reasons = []
    large_cities = {"Chennai","Coimbatore","Madurai","Tiruchirappalli","Salem"}
    if city not in large_cities:
        adj_factor *= 0.7
        reasons.append("Smaller town scaling")
    if place_type == "mall" and dayofweek >= 5:
        adj_factor *= 1.25
        reasons.append("Weekend mall boost")
    if place_type in ["metro_station","bus_stop"] and (7 <= hour <= 9 or 17 <= hour <= 19):
        adj_factor *= 1.35
        reasons.append("Commute peak")
    if event_density > 0.5:
        adj_factor *= (1 + event_density)
        reasons.append("Event density")
    if rain > 5 and place_type in ["beach","tourist_spot","park"]:
        adj_factor *= 0.6
        reasons.append("Heavy rain reduces outdoor visits")
    final_pred = int(max(0, base_pred * adj_factor))
    if final_pred > 4000:
        cat = "🔴 Peak"
    elif final_pred > 1500:
        cat = "🟡 Fair"
    else:
        cat = "🟢 Low"
    st.markdown(f"### 📍 {place_type.title()} — {city}{' / '+location if location else ''}")
    st.metric("Estimated footfall", f"{final_pred} people")
    st.markdown(f"**Category:** {cat}")
    if reasons:
        st.info("Factors: " + ", ".join(reasons))
st.header("Full-day forecast & best visiting window")
if st.button("Show 24-hour Forecast"):
    hours = list(range(24))
    rows = []
    for h in hours:
        rows.append({
            "place_code": place_code,
            "city_code": city_code,
            "temp_celsius": temp,
            "rain_1h": rain,
            "clouds_all": clouds,
            "day": day,
            "hour": h,
            "month": month,
            "dayofweek": dayofweek,
            "event_density": event_density
        })
    df_in = pd.DataFrame(rows)
    missing_cols = [c for c in FEATURES if c not in df_in.columns]
    for c in missing_cols:
        df_in[c] = 0
    for col in FEATURES:
        if col not in df_in.columns:
            df_in[col] = 0
    preds = model.predict(df_in[FEATURES])
    adj_preds = []
    for h, val in enumerate(preds):
        a = 1.0
        if place_type == "mall" and dayofweek >= 5 and 17 <= h <= 21:
            a *= 1.25
        if place_type in ["metro_station","bus_stop"] and (7 <= h <= 9 or 17 <= h <= 19):
            a *= 1.35
        if event_density > 0.5:
            a *= (1 + event_density)
        if rain > 5 and place_type in ["beach","tourist_spot","park"]:
            a *= 0.6
        adj_preds.append(int(max(0, val * a)))
    p25 = np.percentile(adj_preds, 25)
    p75 = np.percentile(adj_preds, 75)
    peak_hours = [i for i, v in enumerate(adj_preds) if v > p75]
    fair_hours = [i for i, v in enumerate(adj_preds) if p25 <= v <= p75]
    low_hours = [i for i, v in enumerate(adj_preds) if v < p25]
    best_hour = int(np.argmin(adj_preds))
    reduction = (max(adj_preds) - min(adj_preds)) / max(1, max(adj_preds)) * 100
    st.success(f"⭐ Best visiting hour: {best_hour}:00  — expected crowd reduction vs peak: {reduction:.1f}%")
    st.write("Peak hours:", ", ".join(map(str, peak_hours)))
    st.write("Fair hours:", ", ".join(map(str, fair_hours)))
    st.write("Low hours:", ", ".join(map(str, low_hours)))
    chart_df = pd.DataFrame({"Hour": hours, "Predicted Crowd": adj_preds}).set_index("Hour")
    st.line_chart(chart_df)
    st.write("---")
    st.write("Note: Predictions use ML baseline × rule-based adjustments (city/event/weather/time).")

