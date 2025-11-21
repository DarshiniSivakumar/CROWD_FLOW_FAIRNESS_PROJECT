import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)


place_types = [
    "mall", "metro_station", "bus_stop", "railway_station",
    "temple", "tourist_spot", "college", "hospital", "theater", "park", "stadium"
]

tn_cities = [
    "Chennai","Coimbatore","Madurai","Tiruchirappalli","Salem","Erode","Tirunelveli",
    "Vellore","Tiruppur","Thoothukudi","Karur","Nagercoil","Cuddalore","Dindigul",
    "Kanchipuram","Kanyakumari","Sivakasi","Pollachi","Ramanathapuram","Villupuram"
]

uploaded_zip = "/mnt/data/metro+interstate+traffic+volume (2).zip"

N = 20000  

rows = []
start_date = datetime(2024,1,1)

def base_by_type(ptype, hour, dow):
    if ptype in ["metro_station", "railway_station", "bus_stop"]:
        base = 3000 * (1 + 0.9 * (7 <= hour <= 9 or 17 <= hour <= 19))
    elif ptype == "mall":
        base = 1800 * (1 + 1.0 * (17 <= hour <= 21))
        if dow >= 5: base *= 1.4
    elif ptype == "airport":
        base = 2500 * (1 + 0.4 * (6 <= hour <= 9 or 18 <= hour <= 22))
    elif ptype == "hospital":
        base = 800
    elif ptype == "college":
        base = 1200 * (1 + 0.8 * (8 <= hour <= 16))
        if dow >= 5: base *= 0.3
    elif ptype == "temple":
        base = 1500 * (1 + 0.9 * (5 <= hour <= 10 or 18 <= hour <= 20))
        if dow >= 5: base *= 1.2
    elif ptype == "theater":
        base = 300 * (1 + 1.3 * (18 <= hour <= 23))
        if dow >= 5: base *= 1.2
    elif ptype == "tourist_spot":
        base = 1000 * (1 + 0.6 * (9 <= hour <= 18))
        if dow >= 5: base *= 1.3
    elif ptype == "park":
        base = 600 * (1 + 0.8 * (16 <= hour <= 20))
    elif ptype == "stadium":
        base = 500 * (1 + 2.0 * (18 <= hour <= 23))  
    else:
        base = 300
    return base
for i in range(N):
    city = random.choice(tn_cities)
    ptype = random.choice(place_types)
    delta_days = random.randrange(0, 365)
    hour = random.randrange(0,24)
    dt = start_date + timedelta(days=delta_days, hours=hour)
    day = dt.day; month = dt.month; dow = dt.weekday()  
    temp = round(np.random.normal(30, 5), 1)  
    rain = max(0.0, np.random.exponential(scale=1.5) * (2.0 if month in [6,7,8,9] else 1.0))
    clouds = int(np.clip(np.random.normal(40, 30), 0, 100))
    event_density = float(np.random.choice([0,0,0,0.2,0.5,1.0], p=[0.6,0.15,0.1,0.08,0.05,0.02]))

    base = base_by_type(ptype, hour, dow)
    weather_factor = 1.0
    if rain > 10 and ptype in ["beach","tourist_spot","park"]:
        weather_factor *= 0.6
    if clouds > 80:
        weather_factor *= 0.9
    if temp > 38 and ptype in ["beach","park"]:
        weather_factor *= 0.85

    crowd = int(max(0, base * (1 + event_density) * weather_factor + np.random.normal(0, base*0.15)))
    rows.append({
        "city": city,
        "place_type": ptype,
        "location": f"{ptype.title()} near {city}",
        "date_time": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "temp_celsius": temp,
        "rain_1h": round(rain,2),
        "clouds_all": clouds,
        "day": day,
        "hour": hour,
        "month": month,
        "dayofweek": dow,
        "event_density": event_density,
        "footfall": crowd
    })

df = pd.DataFrame(rows)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("india_tn_crowd.csv", index=False)
print("Saved india_tn_crowd.csv with", len(df), "rows")
