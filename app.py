import streamlit as st
import pandas as pd
import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor

# Load the saved models
model_point = joblib.load(r'models/model_1.pkl')
knn = joblib.load(r'models/model_2.pkl')
le_user = joblib.load(r'models/model_3.pkl')

# Function to predict location based on future timestamp for all users
def predict_location_for_all_users(future_timestamp):
    future_timestamp = pd.to_datetime(future_timestamp)
    predictions = []

    for user_id in le_user.classes_:
        user_id_encoded = le_user.transform([user_id])[0]
        features = pd.DataFrame([{
            'year': future_timestamp.year,
            'month': future_timestamp.month,
            'day': future_timestamp.day,
            'hour': future_timestamp.hour,
            'minute': future_timestamp.minute,
            'second': future_timestamp.second,
            'day_of_week': future_timestamp.dayofweek,
            'user_id_encoded': user_id_encoded
        }])

        location_point = model_point.predict(features)[0]
        location_point_df = pd.DataFrame([location_point], columns=['longitude', 'latitude'])
        location_name = knn.predict(location_point_df)[0]

        predictions.append({
            'user_id': user_id,
            'location_name': location_name,
            'location_point': location_point.tolist()
        })

    return predictions

# Streamlit app
st.title('Location Prediction Applocation')

# Input for future timestamp
future_timestamp = st.text_input('Enter future timestamp (YYYY-MM-DDTHH:MM:SS)', '2024-06-01T13:00:00')

if st.button('Predict'):
    predictions = predict_location_for_all_users(future_timestamp)
    st.write('Predictions for all users:')
    for prediction in predictions:
        st.write(f'User: {prediction["user_id"]} - Predicted location_name: {prediction["location_name"]} - Predicted location_point: {prediction["location_point"]}')


the code is running fine now i want to some changes like 
# Input for future timestamp
future_timestamp = st.text_input('Enter future timestamp (YYYY-MM-DDTHH:MM:SS)', '2024-06-01T13:00:00')

input for future timestamp i want to pass separately like date and time

and also want to add input for user
