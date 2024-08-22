import streamlit as st
import pandas as pd

# Welcome message with a data emoji
st.write("Welcome to the data view page 📊")

# Load Data

@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv('Telco_churn_cleaned.csv')
    return data

st.dataframe(load_data())