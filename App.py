import streamlit as st
import pandas as pd
import numpy as np
import plotly as plt
import Pages.dashboard as dashboard
import Pages.data as data



st.set_page_config(
    page_title="Classification App",
    page_icon=":hand:",
    layout="wide"
)

# Main Content
st.title("Customer Churn Classification App")
st.markdown(""" This is app uses machine learning to classify whether a customer will churn or not """)

#Key Features
st.subheader("key features")
st.markdown("""
            - Upload your csv file containing sales data
            - Select the desire feature for classification
            - Choose a machine learning model from the drop down menu
            - Click 'Classify' to get  the predicted result
            - The app also provide previous report on sales predictions
            - The report includes matrics like accuracy, precision, recall and F1-Score
          """)

# Menu
st.subheader("App features")
st.markdown("""
- **View Data** : Access priority data
- **Dashboard** : Explore interractive data visuals for insights
""")

# Machine Learning Integration
st.subheader("Machine Learning Integration")
st.markdown("""
- **Model Selection**: Choose between two advanced models for accurte results
- **Seamless Integration**: Integrate predictions into your workflow
- **Probability Estimates**: Gain insights into the likelihoof of prediction                        
""")

# Sidebar content
st.sidebar.write("Need Help❓")

# Main page content
st.markdown("# Contact and GitHub Repository")

# Contact information
st.markdown("""
For collaboration, contact me at [raymutati@gmail.com](mailto:raymutati@gmail.com)
""")

# GitHub repository button
if st.button("Repository on GitHub", help="Visit the GitHub repository"):
    st.write("You can visit the repository at: [GitHub Repository Link](https://github.com/raymondmusyoka/Customer-Churn-Classification-Project.git)")