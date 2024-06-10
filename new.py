import streamlit as st

def page1():
    st.title('Page 1')
    st.write('Welcome to Page 1')

def page2():
    st.title('Page 2')
    st.write('Welcome to Page 2')

pages = {
    'Page 1': page1,
    'Page 2': page2
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio('Go to', list(pages.keys()))

page = pages[selection]
page()
