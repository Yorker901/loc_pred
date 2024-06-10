import streamlit as st

st.sidebar.title('Sidebar Example')
st.sidebar.write('This is a sidebar')

if st.sidebar.checkbox('Show main content'):
    st.write('This is the main content')
