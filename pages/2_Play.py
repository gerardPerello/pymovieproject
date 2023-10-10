import streamlit as st 
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

st.set_page_config(
    page_title="Good luck!",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Settings for seaborn
sns.set_style("whitegrid")
sns.set_context("paper")

# Game states are 
#   0: BEFORE SETUP
#   1: AWAITING SETUP
#   2: DURING TURN
#   3: BETWEEN TURNS
#   4: GAME END

st.header("PyStockMarket")

# GAME NOT JOINED
if 'game_brain' not in st.session_state:
    st.write("A game has not been joined.")

# HAS VISITED SETUP PAGE 
if 'game_brain' in st.session_state:

    st.write(f'You are Player {st.session_state.game_brain.player_id} in Game {st.session_state.game_brain.game_id}')

    # WAITING FOR GAME START
    if st.session_state.game_brain.state == 1: 
        st.markdown("Please wait until game setup is completed")
        st.session_state.game_brain.setup_game()
        st.button(
            'Click here to begin the game'#,
            #on_click=st.session_state.game_brain.begin_game
            )


    # DURING TURN, BETWEEN TURN, GAME END
    if st.session_state.game_brain.state not in [0, 1]: 
        st.write('It is turn', st.session_state.game_brain.turn)
        st.write("The game state is", st.session_state.game_brain.state)

        # DATA
        df = pd.DataFrame(st.session_state.game_brain.currencies)
        st.dataframe(df[0:st.session_state.game_brain.turn+1])

        # PLOT 
        fig, ax = plt.subplots(figsize=(8,3))
        sns.lineplot(
            data=df[0:st.session_state.game_brain.turn+1],
            # hue=st.session_state.curr_data.columns,
            ax=ax,
            markers=['o']
        )
        ax.set_xticks(np.arange(1,st.session_state.game_brain.turn+1))
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlabel('Turn')
        plt.ylabel('Stock Value')
        # plt.xlim(0, st.session_state.game_brain.game.total_turns)
        plt.xlim(0, 20)
        ax.set_ylim(bottom=0)

        sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
        st.pyplot(fig, use_container_width=True)

    # DURING TURN
    if st.session_state.game_brain.state == 2:
        balance = 5000
        st.write(f"Your current balance is {balance:.2f} dollars")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('### Make an order')
            buy_or_sell = st.selectbox('Would you like to buy or sell?', ('Buy', 'Sell'))
            chosen_stock = st.selectbox('Which stock would you like to buy?', df.columns)
            stock_quantity = st.slider('Amount of stock', 0, 300, 25)

            total = stock_quantity * 100
            if buy_or_sell == 'Buy':
                st.write(f"This order will cost you {total} to buy {chosen_stock}")
            if buy_or_sell == 'Sell':
                st.write(f"You will ask for {total} to sell {chosen_stock}")
            
            if total <= balance or buy_or_sell == 'Sell':
                st.button(
                    "Make Order", 
                    on_click=st.session_state.game_brain.send_order
                )
            else:
                st.write("You cannot afford this order.")
                
        with col2:
            df = pd.DataFrame(
                {
                    'Stock': ['USD', 'JPY'],
                    'Number of Shares': [20, 30],
                    'Offer per Share': [2.5, 3],
                    'Total Offer': [2.5*20, 3*30],
                    'Market Offer': [300, 200]        
                }
            )


            st.markdown("### You open orders")
            st.dataframe(df, hide_index=True)

            # Needs to update relatively frequently! 
            st.markdown('### Open Offers this Turn')
            
            st.dataframe(df, hide_index=True)

        # NEXT TURN BUTTON
        st.button(
            'Next Turn', 
            on_click=st.session_state.game_brain.next_turn
            )

        st.markdown('---')
        st.markdown('### Your Portfolio')
        portofolio_df = st.session_state.game_brain.get_portfolio()
        st.dataframe(hide_index=True)

        st.markdown('---')
        st.markdown('### You closed trades last turn')
        # st.session_state.game_brain.get_sell_orders()

    
    if st.session_state.game_brain.state == 3: # BETWEEN TURNS
        st.write('Last turn, the offers were bla bla bla and they closed at bla bla bla.')
        st.write('Please wait while the next turn loads.')
        
        st.button(
            'Click here to move on to the next turn', 
            on_click=st.session_state.game_brain.compute_next_turn
            )

    if st.session_state.game_brain.state == 4:
        st.markdown("## Final Scores")
        scores = st.session_state.game_brain.get_final_scores()

        st.dataframe(scores, hide_index=True)