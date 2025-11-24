import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
df = pd.read_csv("india_tn_crowd.csv")
le_place = LabelEncoder()
le_city = LabelEncoder()
df["place_code"] = le_place.fit_transform(df["place_type"])
df["city_code"] = le_city.fit_transform(df["city"])
FEATURES = [
    "place_code", "city_code", "temp_celsius", "rain_1h",
    "clouds_all", "day", "hour", "month", "dayofweek", "event_density"
]
X = df[FEATURES]
y = df["footfall"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
model = RandomForestRegressor(n_estimators=80, max_depth=20, n_jobs=-1, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print("MAE on test:", mae)
joblib.dump(model, "crowd_model.pkl")
preproc = {"le_place": le_place, "le_city": le_city, "features": FEATURES}
joblib.dump(preproc, "preprocessor.pkl")
print("Saved crowd_model.pkl and preprocessor.pkl")

