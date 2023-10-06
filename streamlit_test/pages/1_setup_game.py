import streamlit as st 
import numpy as np
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Setup",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# SETUP PARAMETERS
MAXTURNS = 20
MAXPLAYERS = 10
MAXSTOCKS = 10

st.write("# Game Setup 📈")

# GET GAME OPTIONS FROM USERS
# - Game settings are stored as session state variables
with st.form('form1'):
    game_name = st.text_input(
        label='Game Name',
        value='',
        placeholder='Name your game!'
    )

    # number of turns
    st.session_state.turncount = st.slider('How many turns do you want to play?', 0, 10, MAXTURNS)
    st.session_state.minutesperturn = st.slider('How many minutes in each turn?', 0, 60, 5)
    st.session_state.secondsperturn = st.session_state.minutesperturn*60

    # amount of money
    st.session_state.startingmoney = st.slider('Starting money for each player', 100, 4000, 1000, step=100)

    # frequency of drastic events
    st.session_state.event_frequency = st.select_slider('How many turns between events?', options=[1, 2, 3])

    # number of stocks
    st.session_state.stockscount = st.slider('How many stocks do you want in your game?', 0, MAXSTOCKS, 5)

    # number of players
    st.session_state.playercount = st.slider('How many people are playing?', 0, MAXPLAYERS, 4)

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write('Game options submitted.')
        st.write(f'Your game will take {st.session_state.turncount} turns and {st.session_state.turncount*st.session_state.minutesperturn} minutes.')


if submitted:
# SEND GAME SETUP TO SNOWFLAKE
# - and get game id
# 

# GET PLAYER IDS FROM SNOWFLAKE

# ESTABLISH SETTINGS AS SESSION STATE VARIABLES

# CALCULATE GET AND STORE CURRENCY DATA IN A PANDAS DATAFRAME
# - which will need to persist
    if 'curr_data' not in st.session_state:

        curr_1 = 20 * np.random.randn(st.session_state.turncount) + 400
        curr_2 = 40 * np.random.randn(st.session_state.turncount) + 300
        curr_data = pd.DataFrame(
            {'USD': curr_1,
            'JPY': curr_2,
            }
        )
        st.session_state.curr_data = curr_data

