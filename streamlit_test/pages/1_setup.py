import streamlit as st 

st.set_page_config(
    page_title="Setup",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed" 
)


st.write("# Game Setup 📈")


# Get game options from user
with st.form('form1'):
    game_name = st.text_input(
        label='Game Name',
        value='',
        placeholder='Name your game!'
    )

    turncount = st.slider('How many turns do you want to play?', 0, 50, 20)
    minutesperturn = st.slider('How many minutes in each turn?', 0, 60, 5)
    secondsperturn = minutesperturn*60

    startingmoney = st.slider('Starting money for each player', 100, 4000, 1000, step=100)

    event_frequency = st.select_slider('How many turns between events?', options=[1, 2, 3])
    stockscount = st.slider('How many stocks do you want in your game?', 0, 30, 15)

    playercount = st.slider('How many people are playing?', 0, 50, 4)

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write('Game options submitted.')
        st.write('Your game will take', turncount, 'turns and ', turncount*minutesperturn, 'minutes.')



# Send game options to snowflake

