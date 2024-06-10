import streamlit as st
import pandas as pd

st.title('Basic Map of India')

# Single point to center the map on India
df = pd.DataFrame({
    'lat': [20.5937],
    'lon': [78.9629]
})

# Display a basic map with Streamlit's built-in map function
st.map(df)
