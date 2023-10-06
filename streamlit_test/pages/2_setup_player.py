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

player_options = [f'player {i}' for i in range(1, st.session_state.playercount+1)]

playing = selectbox(
    'Which player are you?', 
    player_options
)


st.write('You selected:', playing)

st.session_state.playing = playing