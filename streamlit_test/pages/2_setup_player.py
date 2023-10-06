import streamlit as st 
import numpy as np
import pandas as pd
from streamlit_extras.no_default_selectbox import selectbox

st.set_page_config(
    page_title="Setup",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

st.write("# Player Setup")



# Display the chart only if a player ID is selected
if st.session_state.submitted_game_setup:
    # Filter the DataFrame based on the selected player ID
    player_options = [f'player {i}' for i in range(1, st.session_state.playercount+1)]

    playing = selectbox(
        'Which player are you?', 
        player_options
    )
    st.write('You selected:', playing)

    st.session_state.playing = playing
else:
    st.write('Please wait for someone to set up a game.')
