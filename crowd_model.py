import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

# -------------------------------
# 1️⃣ Load CSV
# -------------------------------
df = pd.read_csv(r"C:\Users\Darshini\OneDrive\Desktop\clg\CROWD_FLOW_FAIRNESS_PROJECT\Metro_Interstate_Traffic_Volume.csv")

# -------------------------------
# 2️⃣ Preprocess date_time column
# -------------------------------
df['date_time'] = pd.to_datetime(df['date_time'])

# Extract day, hour, month, day of week
df['day'] = df['date_time'].dt.day
df['hour'] = df['date_time'].dt.hour
df['month'] = df['date_time'].dt.month
df['dayofweek'] = df['date_time'].dt.dayofweek

# -------------------------------
# 3️⃣ Define features and target
# -------------------------------
X = df[['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'day', 'hour', 'month', 'dayofweek']]
y = df['traffic_volume']

# -------------------------------
# 4️⃣ Initialize and train model
# -------------------------------
best_model = RandomForestRegressor(
    n_estimators=50,    # smaller for faster training
    max_depth=12,       # limit depth for speed
    random_state=42,
    n_jobs=-1           # use all CPU cores
)
best_model.fit(X, y)

# -------------------------------
# 5️⃣ Save trained model
# -------------------------------
joblib.dump(best_model, "crowd_model.pkl")
print("🎉 Model saved successfully as crowd_model.pkl")
