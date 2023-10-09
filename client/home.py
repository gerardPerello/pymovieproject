import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title=np.random.choice(['Hi!', 'Hola!', 'Hoi!']),
    page_icon="👋",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

st.write("# Welcome to PyStocks! 📈")

st.markdown(
    """

    🚀 Get set for an adrenaline-fueled ride through the Stock Market! Strap in and unleash your inner tycoon as you navigate the thrilling world of trading. 
    
    You're not just a player; you're a financial virtuoso, ready to conquer the market with your wit and strategy. Buy low, sell high, and watch your investments skyrocket. Will you bet on tech giants or daring startups? The choice is yours! Get ready for heart-pounding moments, epic wins, and maybe a few losses – it's all part of the game. 
    
    So, grab your virtual wallet and let the trading frenzy begin! Good luck, and may your stocks always be bullish! 📈💰
    
    PyStocks is a project by Edoardo Draetta and Gerard Perelló.

    To play, one person needs to set up the game by:
"""
)

st.markdown(
    '''
    **Ready to dive in and get rich? Click the button below:**

    
'''
)

if st.button("⚙️Set up and join a game⚙️"):
    switch_page("setup and join")

st.markdown("![Alt Text](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjVubmh5Nnd5c202NnNoM3pqMW9vNHg4eTYyOHBrcGhxYTVnazR4bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5Ty6JAjSVAiOWXClbw/giphy.gif)")
st.markdown('*PyStocks is a project by Edoardo Draetta and Gerard Perelló.*')