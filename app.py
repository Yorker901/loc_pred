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
def predict_location_for_user(future_timestamp, user_id):
    future_timestamp = pd.to_datetime(future_timestamp)
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

    prediction = {
        'user_id': user_id,
        'location_name': location_name,
        'location_point': location_point.tolist()
    }

    return prediction

# Streamlit app
st.title('Location Prediction Application')

# Input for user
user_id = st.selectbox('Select User', le_user.classes_)

# Input for future date and time
future_date = st.date_input('Enter future date', pd.to_datetime('2024-06-01'))
future_time = st.time_input('Enter future time', pd.to_datetime('13:00:00').time())

if st.button('Predict'):
    # Combine future date and time
    future_timestamp = pd.to_datetime(f'{future_date} {future_time}')
    prediction = predict_location_for_user(future_timestamp, user_id)
    
    st.write('Prediction for the selected user:')
    st.write(f'User: {Predicted location_name: {prediction["location_name"]} Predicted location_point: {prediction["location_point"]}')
