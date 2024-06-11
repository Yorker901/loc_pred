import streamlit as st
import pandas as pd
import joblib
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor

# Check if models exist and load them
model_files = {
    'model_point': r'models/model_1.pkl',
    'knn': r'models/model_2.pkl',
    'le_user': r'models/model_3.pkl'
}

models = {}
for model_name, model_path in model_files.items():
    if os.path.exists(model_path):
        models[model_name] = joblib.load(model_path)
    else:
        st.error(f"Model file {model_path} not found. Please ensure the model files are correctly placed.")
        st.stop()

model_point = models['model_point']
knn = models['knn']
le_user = models['le_user']

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
future_time = st.sidebar.time_input('Enter time', pd.to_datetime('00:00:00').time())

# Input for multiple users
user_ids = st.sidebar.multiselect('Select Users', le_user.classes_)

if st.sidebar.button('Predict'):
    future_timestamp = pd.to_datetime(f'{future_date} {future_time}')
    
    predictions = []
    for user_id in user_ids:
        prediction = predict_location_for_user(future_timestamp, user_id)
        predictions.append(prediction)
    
    st.write('## Predictions for the selected users:')
    
    # Aggregate all locations into a single DataFrame for plotting
    location_data = []
    for prediction in predictions:
        st.markdown(f'### **User ID:** {prediction["user_id"]}')
        st.markdown(f'**Predicted location name:** {prediction["location_name"]}')
        st.markdown(f'**Predicted location point:** {prediction["location_point"]}')
        
        location_data.append({
            'user_id': prediction['user_id'],
            'location_name': prediction['location_name'],
            'timestamp': prediction['timestamp'],
            'latitude': prediction['location_point'][1],
            'longitude': prediction['location_point'][0]
        })
    
    # Convert location data to DataFrame
    location_df = pd.DataFrame(location_data)
    
    # Display the map in Streamlit
    st.map(location_df[['latitude', 'longitude']])

    # Display tooltip information
    for idx, row in location_df.iterrows():
        st.write(f"User ID: {row['user_id']}, Location Name: {row['location_name']}, Location Point: ({row['longitude']}, {row['latitude']}), Timestamp: {row['timestamp']}")
    
    st.write("### Explore the map and interact with other features.")
    
    st.markdown("<div class='footer'>Location Prediction Application © 2024</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='footer'>Location Prediction Application © 2024</div>", unsafe_allow_html=True)
