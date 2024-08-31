import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, RobustScaler, PowerTransformer
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

# Set page config
st.set_page_config(
    page_title="Churn Prediction App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load model components
with open('Models/churn_model_components.pkl', 'rb') as f:
    exported_dict = pickle.load(f)

# Extract the components from the loaded dictionary
preprocessor = exported_dict['preprocessing']['preprocessor']
models = exported_dict['tuned_models']

# Define Prediction Function
def predict(attributes, model_name):
    """Predict churn based on user input and selected model."""
    data = pd.DataFrame([attributes], columns=[
        'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService',
        'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
        'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges'
    ])
    
    # Apply preprocessor to data
    processed_data = preprocessor.transform(data)
    
    # Select the model
    model = models.get(model_name)
    if model is None:
        return None, 0
    
    # Predict and return churn and probability
    pred = model.predict(processed_data)
    prob = model.predict_proba(processed_data)
    
    return pred[0], np.max(prob)

# Save Predictions to History
def save_to_history(user_input, prediction, probability):
    """Save prediction data to a CSV file."""
    history_file = 'data/prediction_history.csv'
    user_input['Prediction'] = 'Churn' if prediction == 1 else 'Not Churn'
    user_input['Probability'] = probability
    
    df = pd.DataFrame([user_input])
    if not pd.io.common.file_exists(history_file):
        df.to_csv(history_file, index=False)
    else:
        df.to_csv(history_file, mode='a', header=False, index=False)

# Streamlit UI
st.title('Customer Churn Prediction Tool')
st.markdown("### Please input the required fields to predict customer churn")

# Model selection
model_name = st.selectbox('Select Model', ['random_forest', 'lightgbm'])

# Input Fields
cols1 = st.columns(3)
cols2 = st.columns(3)
cols3 = st.columns(3)

# Input for Personal Details
with cols1[0]:
    st.header("Personal Details")
    gender = st.selectbox('Gender', ['Male', 'Female'])
    senior_citizen = st.selectbox('Senior Citizen', ['Yes', 'No'])
    partner = st.selectbox('Partner', ['Yes', 'No'])

# Input for Subscription Details
with cols1[1]:
    st.header("Subscription Details")
    contract = st.selectbox('Contract', ['Month-to-month', 'One year', 'Two year'])
    paperless_billing = st.selectbox('Paperless Billing', ['Yes', 'No'])
    payment_method = st.selectbox('Payment Method', ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])

# Input for Service Options
with cols1[2]:
    st.header("Service Options")
    phone_service = st.selectbox('Phone Service', ['Yes', 'No'])
    multiple_lines = st.selectbox('Multiple Lines', ['Yes', 'No', 'No phone service'])

# Input for Internet & Security
with cols2[0]:
    st.header("Internet & Security")
    internet_service = st.selectbox('Internet Service', ['DSL', 'Fiber optic', 'No'])
    online_security = st.selectbox('Online Security', ['Yes', 'No', 'No internet service'])

# Input for Backup & Protection
with cols2[1]:
    st.header("Backup & Protection")
    online_backup = st.selectbox('Online Backup', ['Yes', 'No', 'No internet service'])
    device_protection = st.selectbox('Device Protection', ['Yes', 'No', 'No internet service'])

# Input for Support & Streaming
with cols2[2]:
    st.header("Support & Streaming")
    tech_support = st.selectbox('Tech Support', ['Yes', 'No', 'No internet service'])
    streaming_tv = st.selectbox('Streaming TV', ['Yes', 'No', 'No internet service'])

# Input for Charges & Tenure
with cols3[0]:
    streaming_movies = st.selectbox('Streaming Movies', ['Yes', 'No', 'No internet service'])
    dependents = st.selectbox('Dependents', ['Yes', 'No'])

with cols3[1]:
    st.header("Charges & Tenure")
    monthly_charges = st.slider('Monthly Charges', min_value=0.0, max_value=200.0, value=70.0, step=0.5)
    total_charges = st.slider('Total Charges', min_value=0.0, max_value=10000.0, value=150.0, step=0.5)

with cols3[2]:
    tenure = st.number_input('Tenure (in months)', min_value=0, max_value=100, value=1)

# Capture User Input
user_input = {
    'gender': gender,
    'SeniorCitizen': 'Yes' if senior_citizen == 'Yes' else 'No',
    'Partner': partner,
    'Dependents': dependents,
    'tenure': tenure,
    'PhoneService': phone_service,
    'MultipleLines': multiple_lines,
    'InternetService': internet_service,
    'OnlineSecurity': online_security,
    'OnlineBackup': online_backup,
    'DeviceProtection': device_protection,
    'TechSupport': tech_support,
    'StreamingTV': streaming_tv,
    'StreamingMovies': streaming_movies,
    'Contract': contract,
    'PaperlessBilling': paperless_billing,
    'PaymentMethod': payment_method,
    'MonthlyCharges': monthly_charges,
    'TotalCharges': total_charges
}

# Prediction Logic
if st.button('Predict Churn'):
    prediction, probability = predict(user_input, model_name)
    
    if prediction is not None:
        st.write(f"Prediction: {'Churn' if prediction == 1 else 'Not Churn'}")
        st.write(f"Probability: {probability:.2f}")
        
        # Save the prediction and user data
        save_to_history(user_input, prediction, probability)
    else:
        st.write("Model not found.")
