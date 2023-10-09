import streamlit as st 
import numpy as np
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from client.game_brain import GameBrain
from streamlit_extras.no_default_selectbox import selectbox
from itertools import count


st.set_page_config(
    page_title="Setup and Join",
    page_icon="⚙️",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

if 'game_brain' not in st.session_state:
            st.write("Made a game brain.")
            st.session_state.game_brain = GameBrain()

# SETUP PARAMETERS
MAXTURNS = 20
MAXPLAYERS = 10
MAXSTOCKS = 10

st.write("## Game Setup ⚙️")

# GET GAME OPTIONS FROM USERS
# - Game settings are stored as session state variables
with st.expander("Set up a game"):
    st.write('Select your desired game options and create your game.')
    st.write('The game parameters will be sent to Snowflake and a game will be created.')

    with st.form('form1'):

        game_name = st.text_input(label='Game Name', value='',placeholder='Name your game!')

        # number of turns
        turncount = st.slider('How many turns do you want to play?', 0, 10, MAXTURNS)
        minutesperturn = st.slider('How many minutes in each turn?', 0, 60, 5)
        secondsperturn = minutesperturn*60
        # amount of money
        startingmoney = st.slider('Starting money for each player', 100, 4000, 1000, step=100)

        # frequency of drastic events
        event_frequency = st.select_slider('How many turns between events?', options=[1, 2, 3])

        # number of stocks
        stockcount = st.slider('How many stocks do you want in your game?', 0, MAXSTOCKS, 5)

        # number of players
        playercount = st.slider('How many people are playing?', 0, MAXPLAYERS, 4)

        st.session_state.submitted_game_setup = st.form_submit_button("Submit")

        if st.session_state.submitted_game_setup:
            st.write('Game options submitted.')
            st.write(f'Your game will take {turncount} turns and {turncount*minutesperturn} minutes.')


    if st.session_state.submitted_game_setup:
        # CREATE A GAME BRAIN
        if 'game_brain' not in st.session_state:
            st.write("Made a game brain.")
            st.session_state.game_brain.create_and_push_game(
                name = game_name, 
                total_turns = turncount, 
                sec_per_turn = secondsperturn, 
                starting_money = startingmoney,
                turns_between_events = event_frequency, 
                player_count = playercount, 
                stock_count = stockcount
            )

        # SEND GAME TO SERVER (AND THEN TO SF)
        # st.session_state.game_brain.create_game()




with st.expander("Join a game"):
    st.markdown("## Select Game and Player 🏋️")
    st.markdown("Select an available game, and select your player id")

    if 'game_brain' not in st.session_state: # i.e. you havent just created the game
        st.write("Made a game brain.")
        st.session_state.game_brain.create_and_push_game(
            name = game_name, 
            total_turns = turncount, 
            sec_per_turn = secondsperturn, 
            starting_money = startingmoney,
            turns_between_events = event_frequency, 
            player_count = playercount, 
            stock_count = stockcount
        )
     
    # GET GAME IDs / NAMES 
    open_games = st.session_state.game_brain.get_open_games()
    counter = count(1)
    game_options = {f'game {i+1}':[next(counter), next(counter), next(counter)] for i in range(4)}

    # Choose a game
    game = selectbox(
        'Which active game do you want to join?', 
        game_options
    )
    st.write('You selected:', game)

    # Game is selected
    if game:   
        # GET PLAYER IDS
        player_options = [f'player {i}' for i in game_options[game]]
        
        # Choose a player
        player = selectbox(
            'Which player are you?', 
            player_options
        )

        st.write('You selected:', player)

        # Confirm choice and send to server
        if st.button(f"Join {game} as {player}"):
            st.session_state.game_brain.join_game(game, player)
            # st.session_state.game_brain.state = 1
            switch_page("play")