import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from time import sleep
import altair as alt

sns.set_style("whitegrid")
sns.set_context("paper")

st.set_page_config(
    page_title="Good luck!",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Called when a next turn needs to be computed. 
def next_turn():
    # p_id = st.session_state.player_id
    pass

# Called on turn end to match offers  
def match_offers():
    pass

# Get matched offers and display them 
def display_between_turns():
    st.write('Please wait while we update the database...')
    st.markdown('closed trades:')
    st.dataframe(pd.DataFrame([1,2,3,4]))
    sleep(5)
    pass

# Display the turn
def display_page(state=''):
    col1, col2, col3 = st.columns(3)
    st.markdown(f'Welcome {st.session_state.playing}')
    with col1:
        st.markdown('## Make an order')
    with col2:
        # Needs to update relatively frequently! 
        st.markdown('## Open Offers this Turn')
        df = pd.DataFrame(
            {
                'Stock': ['USD', 'JPY'],
                'Number of Shares': [20, 30],
                'Offer per Share': [2.5, 3],
                'Total Offer': [2.5*20, 3*30],
                'Market Offer': [300, 200]        
            }
        )
        st.dataframe(df, hide_index=True)
    # Maybe.....
    with col3:
        st.markdown('## Chat')


st.header("PyStock Market")

# STOCK MARKET CHART
fig, ax = plt.subplots(figsize=(8,3))
sns.lineplot(
    data=st.session_state.curr_data,
    # hue=st.session_state.curr_data.columns,
    ax=ax
)

sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))

st.pyplot(fig, use_container_width=True)

st.markdown('---')

st.markdown(f'Welcome {st.session_state.playing}')

col1, col2 = st.columns(2)


with col1:
    st.markdown('### Make an order')
with col2:
    # Needs to update relatively frequently! 
    st.markdown('### Open Offers this Turn')
    df = pd.DataFrame(
        {
            'Stock': ['USD', 'JPY'],
            'Number of Shares': [20, 30],
            'Offer per Share': [2.5, 3],
            'Total Offer': [2.5*20, 3*30],
            'Market Offer': [300, 200]        
        }
    )
    st.dataframe(df, hide_index=True)


st.markdown('---')
st.markdown('### Trades closed last turn')
