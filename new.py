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
