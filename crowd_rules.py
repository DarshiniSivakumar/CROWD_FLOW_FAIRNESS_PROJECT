import datetime
import random
def predict_rule_based(place_name):
    place_name = place_name.lower()
    now = datetime.datetime.now()
    hour = now.hour
    weekday = now.weekday()  
    crowd_level = "Moderate"
    score = random.randint(40, 60)
    rules = {
        "college": {
            "peak_hours": range(9, 16),
            "weekdays_only": True
        },
        "mall": {
            "peak_hours": list(range(17, 22)),
            "weekend_boost": 20
        },
        "temple": {
            "peak_hours": list(range(5, 11)) + list(range(18, 21)),
            "weekend_boost": 25
        },
        "beach": {
            "peak_hours": list(range(16, 23)),
            "weekend_boost": 30
        },
        "station": {
            "peak_hours": list(range(7, 10)) + list(range(17, 21)),
            "weekend_drop": -10
        }
    }
    for key in rules:
        if key in place_name:
            r = rules[key]
            if hour in r.get("peak_hours", []):
                score += 25
                crowd_level = "High"
            if r.get("weekdays_only") and weekday >= 5:
                score -= 20
                crowd_level = "Low"
            if weekday >= 5 and "weekend_boost" in r:
                score += r["weekend_boost"]
                crowd_level = "High"
            if weekday >= 5 and "weekend_drop" in r:
                score += r["weekend_drop"]
            score = max(0, min(100, score))
            return score, crowd_level
    return score, crowd_level
