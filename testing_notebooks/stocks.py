import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

st.title('Turn-Based Stock Update Using Callbacks')

turns = 50

c1 = 20 * np.random.randn(turns) + 400
c2 = 15 * np.random.randn(turns) + 200

w1 = np.random.uniform(low=-2, high=2)
w2 = np.random.uniform(low=-2, high=2)

stock_ts = abs(w1*c1 + w2*c2)
events = 0.2*np.random.randn(turns)
# events = np.zeros(turns)

if 'turn' not in st.session_state:
    st.session_state.turn = 0

if 'stock_price' not in st.session_state:
    turn = st.session_state.turn 
    st.session_state.stock_price = []
    st.session_state.stock_price.append(stock_ts[turn] * 2.71828 ** events[turn])

def next_turn():
    st.session_state.turn += 1
    st.session_state.stock_price.append(stock_ts[turn] * 2.71828 ** events[turn])


turn = st.session_state.turn
stock_price = st.session_state.stock_price

fig, ax = plt.subplots(figsize=(4, 2))

x = np.arange(1, turn+2)

sns.lineplot(x=x, y=stock_price, ax=ax, label='stock 1', marker='.')
sns.lineplot(x=x, y=c1[0:turn+1], ax=ax, label='stock 2', )
sns.lineplot(x=x, y=c2[0:turn+1], ax=ax, label='stock 3', )

plt.legend()
plt.ylim(0, 2000)
plt.xlim(1, turns)
st.pyplot(fig)

st.button('Increment', on_click=next_turn)
st.write('Turn = ', st.session_state.turn)
