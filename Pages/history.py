import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Prediction History",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title('Prediction History')

# Load the history data
history_file = 'data/prediction_history.csv'
if pd.io.common.file_exists(history_file):
    df = pd.read_csv(history_file)
    st.write(df)
else:
    st.write("No prediction history available.")