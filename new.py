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
