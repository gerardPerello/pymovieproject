import streamlit as st 
import numpy as np
import pandas as pd
from streamlit_extras.no_default_selectbox import selectbox
from itertools import count

st.set_page_config(
    page_title="Join",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

st.markdown("# Select Game and Player")
st.markdown("Select an available game, and select your player id")

# GET GAME IDs / NAMES 
# I want a dict: game : [players]

counter = count(1)
game_options = {f'game {i+1}':[next(counter), next(counter), next(counter)] for i in range(4)}

# Choose a game
game = selectbox(
    'Which active game do you want to join?', 
    game_options
)
st.write('You selected:', game)
st.session_state.game = game

# Game is selected
if game:
    # GET PLAYER IDS
    player_options = [f'player {i}' for i in game_options[game]]
    
    # Choose a player
    playing = selectbox(
        'Which player are you?', 
        player_options
    )

    st.write('You selected:', playing)
    st.session_state.playing = playing

