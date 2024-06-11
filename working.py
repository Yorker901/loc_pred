import streamlit as st
import pandas as pd
import joblib
import os
import folium
from streamlit_folium import folium_static

# Load the saved models
model_point = joblib.load(r'models/model_1.pkl')
knn = joblib.load(r'models/model_2.pkl')
le_user = joblib.load(r'models/model_3.pkl')

# Function to predict location based on future timestamp for a user
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
        'location_point': location_point.tolist(),
        'timestamp': future_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }

    return prediction

# Streamlit app
st.set_page_config(page_title='Location Prediction', page_icon=':world_map:', layout='wide')
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .title {
        text-align: center;
        color: #4CAF50;
    }
    .footer {
        text-align: center;
        color: #777;
        font-size: 12px;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('Location Prediction Application :world_map:')

# Sidebar for inputs
st.sidebar.title('Input Parameters')

# Input for future date and time
future_date = st.sidebar.date_input('Enter date', pd.to_datetime('2024-06-01'))
future_time = st.sidebar.text_input('Enter time', '00:00:00')

# Input for multiple users
user_ids = st.sidebar.multiselect('Select Users', le_user.classes_)

if st.sidebar.button('Predict'):
    future_timestamp = pd.to_datetime(f'{future_date} {future_time}')
    
    predictions = []
    for user_id in user_ids:
        prediction = predict_location_for_user(future_timestamp, user_id)
        predictions.append(prediction)
    
    st.write('## Predictions for the selected users:')
    
    # Display predictions above the map
    for prediction in predictions:
        st.markdown(f'**User ID:** {prediction["user_id"]}')
        st.markdown(f'**Predicted location name:** {prediction["location_name"]}')
        st.markdown(f'**Predicted location point:** {prediction["location_point"]}')
        # st.markdown(f'**Timestamp:** {prediction["timestamp"]}')
        st.write("---")
    
    # Create a Folium map
    m = folium.Map(location=[28.7041, 77.1025], zoom_start=10)

    # Add markers with tooltips
    for prediction in predictions:
        tooltip = (f"User ID: {prediction['user_id']}<br>"
                   f"Location Name: {prediction['location_name']}<br>"
                   f"Location Point: ({prediction['location_point'][1]}, {prediction['location_point'][0]})<br>"
                   f"Timestamp: {prediction['timestamp']}")
        folium.Marker(
            location=prediction['location_point'][::-1],  # Reverse coordinates for Folium
            tooltip=tooltip
        ).add_to(m)
    
    # Display the map in Streamlit
    folium_static(m)

    st.write("### Explore the map and interact with other features.")
    
    st.markdown("<div class='footer'>Location Prediction Application © 2024</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='footer'>Location Prediction Application © 2024</div>", unsafe_allow_html=True)

