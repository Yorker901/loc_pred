import streamlit as st
import pandas as pd
import joblib
import os
import folium
from streamlit_folium import folium_static
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("streamlit_app.log"),
        logging.StreamHandler()
    ]
)

# Load the saved models
model_path = 'models'
try:
    model_point = joblib.load(os.path.join(model_path, 'model_1.pkl'))
    knn = joblib.load(os.path.join(model_path, 'model_2.pkl'))
    le_user = joblib.load(os.path.join(model_path, 'model_3.pkl'))
    logging.info("Models loaded successfully.")
except Exception as e:
    logging.error(f"Error loading models: {e}")
    st.error(f"Error loading models: {e}")
    st.stop()

# Function to predict location based on future timestamp for a user
def predict_location_for_user(future_timestamp, user_id):
    try:
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

        logging.info(f"Prediction successful for user {user_id}")
        return prediction

    except Exception as e:
        logging.error(f"Error in prediction for user {user_id}: {e}")
        return None

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
future_time = st.sidebar.time_input('Enter time', pd.to_datetime('00:00:00').time())

# Input for multiple users
user_ids = st.sidebar.multiselect('Select Users', le_user.classes_)

if st.sidebar.button('Predict'):
    future_timestamp = pd.to_datetime(f'{future_date} {future_time}')

    predictions = []
    for user_id in user_ids:
        prediction = predict_location_for_user(future_timestamp, user_id)
        if prediction:
            predictions.append(prediction)

    st.write('## Predictions for the selected users:')

    # Display predictions above the map
    for prediction in predictions:
        st.markdown(f'**User ID:** {prediction["user_id"]}')
        st.markdown(f'**Predicted location name:** {prediction["location_name"]}')
        st.markdown(f'**Predicted location point:** {prediction["location_point"]}')
        st.write("---")

    # Create a Folium map centered on the average location
    if predictions:
        avg_lat = sum(pred["location_point"][1] for pred in predictions) / len(predictions)
        avg_lon = sum(pred["location_point"][0] for pred in predictions) / len(predictions)
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

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
    else:
        st.write("No predictions available.")

    st.markdown("<div class='footer'>Location Prediction Application © 2024</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='footer'>Location Prediction Application © 2024</div>", unsafe_allow_html=True)
