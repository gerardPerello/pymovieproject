import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from client.logic.game_brain import GameBrain
from streamlit_extras.no_default_selectbox import selectbox
from itertools import count

st.set_page_config(
    page_title="Setup and Join",
    page_icon="⚙️",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# INITIALIZE AN EMPTY GAME BRAIN

if 'game_brain' not in st.session_state:
    print("CREATING AN EMPTY GAME BRAIN!")
    st.session_state.game_brain = GameBrain()

# SETUP PARAMETERS
MAXTURNS = 20
MAXPLAYERS = 10
MAXSTOCKS = 10

if 'game_brain' in st.session_state:


    st.markdown("## Use this page to set up and join a game")
    # GET GAME OPTIONS AND CREATE A GAME
    with st.expander("Game Setup ⚙️"):

        st.write('Select your desired game options and create your game.')
        st.write('The game parameters will be sent to Snowflake and a game will be created.')

        with st.form('form1'): # Gather settings

            game_name = st.text_input(label='Game Name', value='', placeholder='Name your game!')

            # number of turns
            turncount = st.slider('How many turns do you want to play?', 0, 10, MAXTURNS)

            # turn time
            # minutesperturn = st.slider('How many minutes in each turn?', 0, 60, 5)
            secondsperturn = 0

            # amount of money
            startingmoney = st.slider('Starting money for each player', 100, 4000, 1000, step=100)

            # frequency of drastic events
            event_frequency = st.select_slider('How many turns between events?', options=[1, 2, 3])

            # number of stocks
            stockcount = st.slider('How many stocks do you want in your game?', 0, MAXSTOCKS, 5)

            # number of players
            playercount = st.slider('How many people are playing?', 0, MAXPLAYERS, 4)

            # Submit button
            st.session_state.submitted_game_setup = st.form_submit_button("Submit")

            if st.session_state.submitted_game_setup:
                st.write('Game options submitted.')
                # st.write(f'Your game will take {turncount} turns and {turncount*minutesperturn} minutes.')


        if st.session_state.submitted_game_setup:
            # CREATE A GAME BRAIN AND SEND IT TO SNOWFLAKE
            print("CREATING A GAME AND PUSHING IT TO SNOWFLAKE!")
            st.session_state.game_brain.create_and_push_game(
                name = game_name,
                total_turns = turncount,
                sec_per_turn = secondsperturn,
                starting_money = startingmoney,
                turns_between_events = event_frequency,
                player_count = playercount,
                stock_count = stockcount
            )

            # SUCCESS MESSAGE?
            st.write("Game successfully created.")


    # SELECT AN AVAILABLE GAME AND JOIN IT
    with st.expander("Select Game and Player 🏋️"):
        st.markdown("Select an available game, then select a player id")

        #########Gerard: WHAT???
        """if 'game_brain' not in st.session_state: # i.e. you havent just created the game
            st.write("Made a game brain.")
            st.session_state.game_brain.create_and_push_game(
                name = game_name,
                total_turns = turncount,
                # sec_per_turn = secondsperturn,
                starting_money = startingmoney,
                turns_between_events = event_frequency,
                player_count = playercount,
                stock_count = stockcount
            )"""

        # GET GAME IDs / NAMES

        if not st.session_state.game_brain.open_games_req:
            open_games = st.session_state.game_brain.get_open_games()
        #counter = count(1) ################G: WHAT?

        # Choose a game
        game_id = selectbox(
            'Which active game do you want to join?',
            open_games.keys()
        )
        st.write('You will join Game_', game_id)

        if game_id: # Game is selected

            # Choose a player
            player_id = selectbox(
                'Which player are you?',
                open_games[game_id]
            )

            st.write('You are the Player_', player_id)

            # Confirm choice and send to server
            if st.button(f"Join to Game_{game_id} as {player_id}"):
                st.session_state.game_brain.join_game(game_id, player_id)
                st.session_state.game_brain.state = 1
                switch_page("play")
