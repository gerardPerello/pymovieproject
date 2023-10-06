import streamlit as st
import time

st.set_page_config(
    page_title="Timer",
    page_icon="⏲️",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

ph = st.empty()
N = 5*60
for secs in range(N,0,-1):
    mm, ss = secs//60, secs%60
    ph.metric("Countdown", f"{mm:02d}:{ss:02d}")
    time.sleep(1)