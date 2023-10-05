import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(
    page_title="Hoi!",
    page_icon="👋",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

st.write("# Welcome to PyStocks! 📈")

st.sidebar.success("Navigate between pages using this sidebar.")


st.markdown(
    """
    PyStocks is a project by Edoardo Draetta and Gerard Perelló.
"""
)

if st.button("Click here to begin playing"):
    switch_page("play")
if st.button("Click here to set up a game!"):
    switch_page("Setup")
