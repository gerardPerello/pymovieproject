import streamlit as st 
import numpy as np
import pandas as pd
from streamlit_extras.no_default_selectbox import selectbox
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# session variables
if 'game_state' not in st.session_state:
    # Game states are 
    # 0: NOT STARTED
    # 1: DURING TURN
    # 2: BETWEEN TURNS
    st.session_state.game_state = 0

# Functions
if 'turn' not in st.session_state:
    st.session_state.turn = 0

def increment_turn():
    # How will this work with game brain?
    if st.session_state.turn < st.session_state.turncount:
        st.session_state.turn += 1
        st.session_state.game_state = 2 # BETWEEN TURNS

def begin_game():
    st.session_state.game_state = 1

def reset_turn():
    # How will this work with game brain?
    st.session_state.game_state = 1 # DURING TURNS

# GUI
st.markdown("# Next Turn Functionality")

if st.session_state.game_state == 0: # NOT STARTED
    st.button('Click here to begin the game', on_click=begin_game)

if st.session_state.game_state != 0:
    # DATA
    st.dataframe(st.session_state.curr_data.iloc[0:st.session_state.turn+1, :])

    # PLOT 
    fig, ax = plt.subplots(figsize=(8,3))
    sns.lineplot(
        data=st.session_state.curr_data.iloc[0:st.session_state.turn+1, :],
        # hue=st.session_state.curr_data.columns,
        ax=ax,
        markers=['o']
    )
    ax.set_xticks(np.arange(1,st.session_state.turn+1))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel('Turn')
    plt.ylabel('Stock Value')
    plt.xlim(0, st.session_state.turncount)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    st.pyplot(fig, use_container_width=True)


if st.session_state.game_state == 1: # DURING TURN
    
    # NEXT TURN BUTTON
    st.button('Next Turn', on_click=increment_turn)
    st.write('It is turn', st.session_state.turn)

   
if st.session_state.game_state == 2: # BETWEEN TURNS
    st.write('Last turn, the offers were bla bla bla and they closed at bla bla bla.')
    st.write('Please wait while the next turn loads.')
    st.button('Click here to move on to the next turn', on_click=reset_turn)
