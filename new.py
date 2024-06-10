import streamlit as st
import pandas as pd
import pydeck as pdk

st.title('Map Visualization of India')

# Sample data with locations in India
df = pd.DataFrame({
    'lat': [28.6139, 19.0760, 13.0827],
    'lon': [77.2090, 72.8777, 80.2707],
    'name': ['New Delhi', 'Mumbai', 'Chennai']
})

# Display a basic map with Streamlit's built-in map function
st.map(df)

st.write('Interactive Map with PyDeck:')
# PyDeck map centered on India
st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=20.5937,
        longitude=78.9629,
        zoom=4,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=df,
           get_position='[lon, lat]',
           radius=20000,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
    ],
))
