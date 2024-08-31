import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Setting up the page
st.set_page_config(page_title="Data Dashboard", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")

# Welcome message with a smile emoji
st.write("Welcome to your dashboard 😊")

# Load Data

@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv('Telco_churn_cleaned.csv')
    # Convert 'Churn' from 'Yes/No' to 1/0 for analysis
    data['Churn'] = data['Churn'].map({'Yes': 1, 'No': 0})
    return data

data= load_data()

# Display the DataFrame in the Streamlit app
st.dataframe(data)

# Convert 'gender' to numeric.
if 'gender' in data.columns:
    data['gender'] = data['gender'].map({'Male': 0, 'Female': 1}).fillna(-1)

numeric_df = data.select_dtypes(include=['float64', 'int64'])

st.title('Comprehensive Data Dashboard')

# Analytics Dashboard
st.header("Analytics Dashboard")
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    churn_rate = data[data['Churn'] == 'Yes'].shape[0] / \
        data.shape[0] * 100 if 'Churn' in data.columns else 0
    st.metric("Churn Rate", f"{churn_rate:.2f}%")

with kpi2:
    arpu = data['MonthlyCharges'].mean() if 'MonthlyCharges' in data.columns else 0
    st.metric("Average Revenue Per User", f"${arpu:.2f}")

with kpi3:
    average_tenure = data['tenure'].mean() if 'tenure' in data.columns else 0
    st.metric("Average Customer Tenure", f"{average_tenure:.1f} months")

# Exploratory Data Analysis Section
st.header("Exploratory Data Analysis")
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Distribution of Monthly Charges")
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.histplot(numeric_df['MonthlyCharges'], kde=True, color='blue', ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("Distribution of Tenure")
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.histplot(numeric_df['tenure'], kde=True, color='green', ax=ax)
    st.pyplot(fig)

with col3:
    st.subheader("Churn Rate Pie Chart")
    churn_counts = data['Churn'].value_counts()
    fig, ax = plt.subplots(figsize=(3, 3))
    churn_counts.plot(kind='pie', labels=[
                      'Retained', 'Churned'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'], ax=ax)
    ax.set_ylabel('')
    st.pyplot(fig)

new_col1, new_col2 = st.columns(2)
with new_col1:
    st.subheader("Payment Method vs Churn")
    payment_churn = pd.crosstab(data['PaymentMethod'], data['Churn'])
    fig, ax = plt.subplots(figsize=(4, 3))  
    payment_churn.plot(kind='bar', stacked=True, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45,
                       ha='right', fontsize=9)
    ax.set_ylabel('Counts', fontsize=10) 
    ax.set_xlabel('Payment Method', fontsize=10)
    st.pyplot(fig)

with new_col2:
    st.subheader("Contract vs Churn")
    contract_churn = pd.crosstab(data['Contract'], data['Churn'])
    fig, ax = plt.subplots(figsize=(4, 3))  
    contract_churn.plot(kind='bar', stacked=True, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45,
                       ha='right', fontsize=9) 
    ax.set_ylabel('Counts', fontsize=10) 
    ax.set_xlabel('Contract', fontsize=10)  
    st.pyplot(fig)