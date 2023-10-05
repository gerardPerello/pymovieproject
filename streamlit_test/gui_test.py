import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# game setup
turns = 20

def game_setup():
    stock_ts = 20 * np.random.randn(turns) + 400
    events = 0.2*np.random.randn(turns)
    return stock_ts, events

# Toy Data
sell_offers = {
    'Amount': [15, 20],
    'Offers': [255.25, 120.54],
    'Players': ['player 1', 'player 2']

}
offers_df = pd.DataFrame(sell_offers)

stock_ts, events = game_setup()

# Session variables
if 'turn' not in st.session_state:
    st.session_state.turn = 0

if 'stock_price' not in st.session_state:
    t = st.session_state.turn 
    st.session_state.stock_price = []
    st.session_state.stock_price.append(stock_ts[t] * 2.71828 ** events[t])


# Called when the next turn button is pressed
def next_turn():
    if st.session_state.turn < turns:
        st.session_state.turn += 1
        t = st.session_state.turn 
        st.session_state.stock_price.append(stock_ts[t] * 2.71828 ** events[t])


# GUI

# main page
st.title("Welcome to PyStocks")

t = st.session_state.turn
sp = st.session_state.stock_price
my_bar = st.progress(t/turns)

tab1, tab2, tab3 = st.tabs(["Stock Market", "Portfolio", "Game Setup"])

with tab1:
    col1, col2 = st.columns([2,1])
    with col1:
        fig, ax = plt.subplots(figsize=(4, 2))
        sns.lineplot(x=np.arange(1, len(sp)+1), y=sp, ax=ax, label='stock 1', marker='.')
        plt.legend()
        plt.ylim(0, 2000)
        plt.xlim(1, turns)
        st.pyplot(fig)
        st.button('Increment', on_click=next_turn)
        st.write('Turn = ', t)

    with col2:
        st.subheader("Offers")
        st.dataframe(data=offers_df, hide_index=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("City", ["AnotherCity1", "AnotherCity2"])
    with col2:
        st.selectbox("District", ["AnotherDistrict1", "AnotherDistrict2"])

with tab3:
    if st.button('Reset Game'):
        st.text('resetting game!')
        stock_ts, events = game_setup()

        st.session_state.turn = 1
        st.session_state.stock_price = []
        t = st.session_state.turn 
        st.session_state.stock_price.append(stock_ts[t] * 2.71828 ** events[t])

    
# Sidebar
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

# Expander
expander = st.expander("See rules")
expander.write('This is a stock trading game made in python.')
