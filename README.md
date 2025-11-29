# CROWD_FLOW_FAIRNESS_PROJECT

# Crowd Flow Fairness Prediction
This project predicts hourly crowd levels across public places in Tamil Nadu and evaluates fairness across different location categories. It includes data generation, model training, and a Streamlit-based interactive dashboard.

### Project Summary
-The goal is to build a machine learning system that:
-Predicts footfall (crowd level) based on weather, events, and time features
-Ensures fairness across different place types (e.g., malls, temples, bus stands)
-Provides a real-time dashboard for predictions and insights
-A Random Forest model is used along with custom preprocessing.

### Live Demo
- Streamlit App:
https://crowdflowfairnessproject-obh6nsij9tsyrzh4gigvwe.streamlit.app/

### How the System Works

## 1. Dataset Creation
-Synthetic but realistic Tamil Nadu crowd data was generated using:
-Weather attributes
-Hour/day/month patterns
-Place categories
-Event density
**File:** india_tn_crowd.csv

## 2. Model Training
A Random Forest Regressor is trained using the following features:
-Feature	Purpose
-place_code	Encoded place type
-city_code	Encoded city names
-temp_celsius	Temperature
-rain_1h	Rain intensity
-clouds_all	Cloud coverage (%)
-day/hour/month/dayofweek	Time-based patterns
-event_density	Indicates festivals/events affecting crowd
**Artifacts produced:**
-crowd_model.pkl
-preprocessor.pkl

## 3. Streamlit Web App
The interface (app.py) includes:
-Real-time crowd prediction
-Full day forecast
-Peak/low hour detection
-Fairness evaluation across categories
-Clean visual insights

### Key Feature Explanations
## Event Density
A numerical factor indicating:
-Festivals
-Local events
-Weekend rush
-Special occasions
This helps the model simulate realistic spikes in footfall.

## Cloud Coverage
-% of sky covered by clouds (0–100)
-Impacts outdoor crowd behaviour
-These descriptions are added in the README because they explain why these features are part of the model, not because users need to enter them manually.

### Repository Structure
app.py                          # Streamlit interface
train_model.py                  # Model training script
generate_dataset.py             # Synthetic data generator
crowd_model.py                  # Model wrapper functions
crowd_rules.py                  # Simple rule-based checks
india_tn_crowd.csv              # Final dataset
crowd_model.pkl                 # Trained ML model
preprocessor.pkl                # Encoders & feature transformers
requirements.txt                # Python dependencies
CrowdFlowFairness_Project.ipynb # Notebook with initial analysis and steps
Metro_Interstate_Traffic_Volume.csv # Reference dataset (not used in app)
README.md

### Additional Clarifications
CrowdFlowFairness_Project.ipynb-Contains initial exploratory analysis, testing, and step-by-step development.

## Files used directly in the Streamlit app
train_model.py
generate_dataset.py
app.py
requirements.txt
preprocessor.pkl
crowd_model.pkl
india_tn_crowd.csv

## Other files
crowd_model.py, crowd_rules.py → Helper logic
Metro_Interstate_Traffic_Volume.csv → Reference dataset used earlier in testing (not required for the app)

### Running Locally
-pip install -r requirements.txt
-streamlit run app.py

### Author
Darshini Sivakumar
