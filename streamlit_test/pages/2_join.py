import streamlit as st 
import numpy as np
import pandas as pd
from streamlit_extras.no_default_selectbox import selectbox

st.set_page_config(
    page_title="Join",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

st.markdown("# Select Game and Player")
st.markdown("Select an available game, and select your player id")

# Display the chart only if a player ID is selected
if st.session_state.submitted_game_setup:

    # Choose a game
    game_options = [f'game {i}' for i in range(1, st.session_state.playercount+1)]
    game = selectbox(
        'Which player are you?', 
        game_options
    )
    st.write('You selected:', game)
    st.session_state.game = game

    # Choose a player
    player_options = [f'player {i}' for i in range(1, st.session_state.playercount+1)]
    playing = selectbox(
        'Which player are you?', 
        player_options
    )
    st.write('You selected:', playing)
    st.session_state.playing = playing

else:
    st.write('Please wait for someone to set up a game.')
