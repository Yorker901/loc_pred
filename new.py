import streamlit as st
import pandas as pd
import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor

# Load the saved models
model_point = joblib.load(r'models/model_1.pkl')
knn = joblib.load(r'models/model_2.pkl')
le_user = joblib.load(r'models/model_3.pkl')

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
            'location_point': location_point.tolist()
        }

        return prediction
    except Exception as e:
        st.error(f'Error in prediction: {e}')
        return None

# Streamlit app
st.title('Location Prediction Application')

# Input for future date and time
future_date = st.date_input('Enter date', pd.to_datetime('2024-06-01'))

# Input for future time
future_time = st.text_input('Enter time', '00:00:00')

# Input for user
user_id = st.selectbox('Select User', le_user.classes_)

if st.button('Predict'):
    # Combine future date and time
    future_timestamp = pd.to_datetime(f'{future_date} {future_time}')
    prediction = predict_location_for_user(future_timestamp, user_id)
    
    if prediction:
        st.markdown(f'**Predicted location name:** {prediction["location_name"]}')
        st.markdown(f'**Predicted location point:** {prediction["location_point"]}')


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Example Data
df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 20, 30, 40]
})

st.title('Data Visualization Example')

st.write('Line Chart:')
st.line_chart(df)

st.write('Bar Chart:')
st.bar_chart(df)

st.write('Area Chart:')
st.area_chart(df)



import streamlit as st
import pandas as pd
import pydeck as pdk

st.title('Map Visualization Example')

df = pd.DataFrame({
    'lat': [37.7749, 40.7128, 34.0522],
    'lon': [-122.4194, -74.0060, -118.2437],
    'name': ['San Francisco', 'New York', 'Los Angeles']
})

st.map(df)

st.write('Interactive Map with PyDeck:')
st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=37.7749,
        longitude=-122.4194,
        zoom=10,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=df,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
    ],
))

import streamlit as st

st.sidebar.title('Sidebar Example')
st.sidebar.write('This is a sidebar')

if st.sidebar.checkbox('Show main content'):
    st.write('This is the main content')

