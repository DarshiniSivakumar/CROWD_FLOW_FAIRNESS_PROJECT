import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
df = pd.read_csv(r"C:\Users\Darshini\OneDrive\Desktop\clg\CROWD_FLOW_FAIRNESS_PROJECT\Metro_Interstate_Traffic_Volume.csv")
df['date_time'] = pd.to_datetime(df['date_time'])
df['day'] = df['date_time'].dt.day
df['hour'] = df['date_time'].dt.hour
df['month'] = df['date_time'].dt.month
df['dayofweek'] = df['date_time'].dt.dayofweek
X = df[['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'day', 'hour', 'month', 'dayofweek']]
y = df['traffic_volume']
best_model = RandomForestRegressor(
    n_estimators=50,    # smaller for faster training
    max_depth=12,       # limit depth for speed
    random_state=42,
    n_jobs=-1           # use all CPU cores
)
best_model.fit(X, y)
joblib.dump(best_model, "crowd_model.pkl")
print("🎉 Model saved successfully as crowd_model.pkl")
