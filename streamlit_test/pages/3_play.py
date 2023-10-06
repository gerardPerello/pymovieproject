import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(
    page_title="Good luck!",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

st.header("PyStock Market")

# STOCK MARKET CHART
st.line_chart(
    data=st.session_state.curr_data,
    y=st.session_state.curr_data.columns,
    use_container_width=True
)

st.markdown('---')
st.markdown(f'Welcome {st.session_state.playing}')

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('## Make an order')

with col2:
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
    st.dataframe(df)

with col3:
    st.markdown('## Chat')