import streamlit as st

# Streamlit app
st.title('Page Version Switcher')

# Button to switch to Version 1
if st.button('Switch to Version 1'):
    st.header('Version 1 Content')
    st.write('Welcome to Version 1 of the page! You pressed the button to switch.')

# Button to switch to Version 2
if st.button('Switch to Version 2'):
    st.header('Version 2 Content')
    st.write('Welcome to Version 2 of the page! You pressed the button to switch.')
