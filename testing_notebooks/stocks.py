import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

'''
This script is a demo of how stock prices could be computed from starting data
and altered by random events. 

The streamlit interface plots the stock each turn, and a button controls turn
progression.
'''

st.title('Turn-Based Stock Update Using Callbacks')

turns = 50 # total number of turns 

# Random noise to simulate stock
c1 = 20 * np.random.randn(turns) + 400
c2 = 15 * np.random.randn(turns) + 200

# A random weight for each weight
w1 = np.random.uniform(low=-2, high=2)
w2 = np.random.uniform(low=-2, high=2)

# The stock timeseries is calculated as a linear combination of the 
# two timeseries above. 

stock_ts = abs(w1*c1 + w2*c2)

# Random events affect the stock price
events = 0.2*np.random.randn(turns)
# events = np.zeros(turns)


# Session variables
if 'turn' not in st.session_state:
    st.session_state.turn = 0

if 'stock_price' not in st.session_state:
    t = st.session_state.turn 
    st.session_state.stock_price = []
    st.session_state.stock_price.append(stock_ts[t] * 2.71828 ** events[t])

# Called when the next turn button is pressed
def next_turn():
    st.session_state.turn += 1
    t = st.session_state.turn 
    st.session_state.stock_price.append(stock_ts[t] * 2.71828 ** events[t])

# Plot the stock price this turn
t = st.session_state.turn
sp = st.session_state.stock_price

fig, ax = plt.subplots(figsize=(4, 2))

x = np.arange(1, t+2)

sns.lineplot(x=x, y=sp, ax=ax, label='stock 1', marker='.')
sns.lineplot(x=x, y=c1[0:t+1], ax=ax, label='stock 2', )
sns.lineplot(x=x, y=c2[0:t+1], ax=ax, label='stock 3', )

plt.legend()
plt.ylim(0, 2000)
plt.xlim(1, turns)
st.pyplot(fig)

st.button('Increment', on_click=next_turn)
st.write('Turn = ', t)