from time import sleep

from scripts import forex_api_connection
import datetime as dt
import pandas as pd
import streamlit as st
from scripts.app import controller
from scripts.app.logic import game_logic
import os


def option1(url, date_from, date_to, n_currencies):
    st.session_state.messages.append("Loading Data From Internet")

    currencies, currencies_dict = forex_api_connection.get_currencies_names(n_currencies)

    total_data = []

    delta = dt.timedelta(days=1)

    while date_from <= date_to:
        params = forex_api_connection.define_params(date_from, currencies)

        data = forex_api_connection.get(url, params)

        total_data.append(data)

        date_from += delta

        sleep(1)

    return forex_api_connection.format_data(total_data, currencies_dict)


def option2(url):
    st.session_state.messages.append("Loading Data From Computer")
    return pd.read_json(url)


def option3(data):
    st.session_state.messages.append("Displaying DataSet")
    data_list = data.to_dict(orient='records')
    message = controller.create_forex_history(data_list)
    st.session_state.messages.append(message)

    st.dataframe(data)


def option4():
    st.session_state.messages.append("Push Currencies")
    currencies_df = pd.read_json('./data/currencies/currencies.json')
    st.dataframe(currencies_df)
    data_list = currencies_df.to_dict(orient='records')
    message = controller.create_currency(data_list)
    st.session_state.messages.append(message)


st.title("STOCK GAME")

if 'data' not in st.session_state:
    st.session_state.data = None

if 'messages' not in st.session_state:
    st.session_state.messages = []

col_url, col_date_from, col_date_to, col_n_currencies = st.columns(4)

with col_url:
    URL = st.text_input("URL", value="http://api.currencylayer.com/historical")
with col_date_from:
    date_from = st.date_input("date_from", value=dt.date(2011, 1, 1))
with col_date_to:
    date_to = st.date_input("date_to", value=dt.date(2011, 1, 1))
with col_n_currencies:
    n_currencies = st.selectbox("n_currencies", list(range(161)), index=5)

if st.button("Load From URL"):
    st.session_state.data = option1(URL, date_from, date_to, n_currencies)

col_url_local, col_button_local_selector = st.columns(2)

with col_url_local:
    URL_local = st.text_input("URL LOCAL TO GET DATA", value="./data/api_currencies/output.json")

# with col_button_local_selector:
# uploaded_file = st.file_uploader("Select file", type=["json"])

# if uploaded_file is not None:
# Save the uploaded file to a temporary directory

# Get the local file path
#    URL_local = os.path.abspath(os.path.join(uploaded_file.name))"""

if st.button("Load From Local"):
    st.session_state.data = option2(URL_local)

if st.button("Display Data"):
    if st.session_state.data is not None:
        option3(st.session_state.data)
    else:
        st.warning("Please select an option before using Option 3.")

if st.button("Option 4"):
    option4()

indexed_messages = [f"{i + 1}: {message}" for i, message in enumerate(st.session_state.messages)]

message_text = "\n".join(indexed_messages)

st.text_area("Messages:", message_text, height=200)
