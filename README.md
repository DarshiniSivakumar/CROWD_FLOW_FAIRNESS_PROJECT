# Crowd Flow Fairness Prediction

This project predicts hourly crowd levels across public places in Tamil Nadu and evaluates fairness across different location categories. It includes data generation, model training, and a Streamlit-based interactive dashboard.

---

## Project Summary

The goal of this project is to build a machine learning system that:

- Predicts footfall (crowd level) based on weather, events, and time features.  
- Ensures fairness across different place types, such as malls, temples, and bus stands.  
- Provides a real-time dashboard for predictions and insights.  
- Uses a Random Forest model along with custom preprocessing.

---

## Live Demo

Streamlit App:  
https://crowdflowfairnessproject-obh6nsij9tsyrzh4gigvwe.streamlit.app/

---

## How the System Works

### 1. Dataset Creation

A synthetic but realistic Tamil Nadu crowd dataset was generated using:
- Weather attributes  
- Hour, day, and month patterns  
- Place categories  
- Event density  
Dataset File: `india_tn_crowd.csv`

---

### 2. Model Training

A Random Forest Regressor is trained using the following features:

| Feature        | Purpose / Meaning                       |
|----------------|-----------------------------------------|
| `place_code`   | Encoded place type                      |
| `city_code`    | Encoded city names                      |
| `temp_celsius` | Temperature                             |
| `rain_1h`      | Rain intensity                          |
| `clouds_all`   | Cloud coverage (%)                      |
| `day`          | Day of the month                        |
| `hour`         | Hour of the day                         |
| `month`        | Month                                   |
| `dayofweek`    | Day of the week                         |
| `event_density`| Indicates festivals or events affecting crowd |

Artifacts produced:

- `crowd_model.pkl` — trained Random Forest model  
- `preprocessor.pkl` — encoders and feature transformers

---

### 3. Streamlit Web App

The app provides:
- Real-time crowd prediction  
- Full day forecast  
- Peak and low hour detection  
- Fairness evaluation across categories  
- Clean visual insights

---

## Key Feature Explanations

### Event Density

A numerical factor that represents:
- Festivals  
- Local events  
- Weekend rush  
- Special occasions  
This helps the model simulate realistic spikes in footfall.

### Cloud Coverage

Percentage of sky covered by clouds (0–100):

- Impacts outdoor crowd behaviour  
- Used to explain predictions, not required for manual input

---

## Repository Structure

```

CROWD_FLOW_FAIRNESS_PROJECT/
│
├── app.py                        # Streamlit interface
├── train_model.py                # Model training script
├── generate_dataset.py           # Synthetic data generator
├── crowd_model.py                # Model wrapper/helper functions
├── crowd_rules.py                # Simple rule-based checks
├── india_tn_crowd.csv            # Final dataset
├── crowd_model.pkl               # Trained ML model
├── preprocessor.pkl              # Encoders & feature transformers
├── requirements.txt              # Python dependencies
├── CrowdFlowFairness_Project.ipynb # Notebook with initial analysis
├── Metro_Interstate_Traffic_Volume.csv # Reference dataset (not used in app)
└── README.md                     # Documentation

````

## Additional Clarifications

- `CrowdFlowFairness_Project.ipynb` contains initial exploratory analysis, testing, and step-by-step development.  
- Files used directly in the Streamlit app: `train_model.py`, `generate_dataset.py`, `app.py`, `requirements.txt`, `preprocessor.pkl`, `crowd_model.pkl`, `india_tn_crowd.csv`.  
- Other files: `crowd_model.py`, `crowd_rules.py` — helper logic.  
- `Metro_Interstate_Traffic_Volume.csv` — reference dataset used earlier in testing, not required for the app.

---

## Running Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
````

2. Run the Streamlit app:

```bash
streamlit run app.py
```

## Author

Darshini Sivakumar
