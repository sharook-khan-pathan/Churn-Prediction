import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the saved model, scaler, and imputer
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
imputer = joblib.load('imputer.pkl')

# Streamlit App UI
st.title('Customer Churn Prediction')
st.write('Upload a CSV file with customer data to predict churn.')

# File uploader for CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the uploaded CSV file into a DataFrame
    test_data = pd.read_csv(uploaded_file)
    #st.write('Uploaded Data:')
    #st.dataframe(test_data)

    # Ensure the CSV has the correct columns
    required_columns = ['CustomerID', 'Age', 'Tenure', 'Usage Frequency', 'Support Calls', 
                        'Payment Delay', 'Total Spend', 'Last Interaction', 'Gender_Male', 
                        'Subscription Type_Premium', 'Subscription Type_Standard', 
                        'Contract Length_Monthly', 'Contract Length_Quarterly']
    
    if all(col in test_data.columns for col in required_columns):
        # Extract the features (excluding the target variable 'Churn')
        input_data = test_data[required_columns]
        
        # Preprocess the data
        input_data_scaled = scaler.transform(input_data)  # Scale the data
        input_data_imputed = imputer.transform(input_data_scaled)  # Impute missing values
        
        # Make predictions using the loaded model
        predictions = model.predict(input_data_imputed)

        # Add predictions to the DataFrame
        test_data['Predicted Churn'] = predictions
        
        # Display the predictions
        st.write('Predicted Churn for Customers:')
        st.dataframe(test_data[['CustomerID', 'Predicted Churn']])

        # Display customers who are predicted to churn (Predicted Churn = 1)
        churned_customers = test_data[test_data['Predicted Churn'] == 1]
        
        if not churned_customers.empty:
            st.write('Customers Predicted to Churn:')
            st.dataframe(churned_customers[['CustomerID', 'Predicted Churn']])
        else:
            st.write('No customers are predicted to churn.')
    else:
        st.error('The uploaded CSV file is missing required columns.')

