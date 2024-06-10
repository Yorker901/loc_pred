import streamlit as st
import pandas as pd

st.title('File Upload Example')

uploaded_file = st.file_uploader('Choose a file')
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write('File Contents:')
    st.write(df)
