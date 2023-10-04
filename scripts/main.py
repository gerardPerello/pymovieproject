from time import sleep

import api_connection
import datetime as dt
import pandas as pd
import credentials
import snowflake_connection as snw
import streamlit as st


def option1(url, date_from, date_to, n_currencies):
    st.session_state.messages.append("Loading Data From Internet")

    currencies = api_connection.get_currencies_names(n_currencies)

    total_data = []

    delta = dt.timedelta(days=1)

    while date_from <= date_to:
        params = api_connection.define_params(date_from, currencies)

        data = api_connection.get(url, params)

        total_data.append(data)

        date_from += delta

        sleep(1)

    return api_connection.format_data(total_data)


def option2():
    st.session_state.messages.append("Loading Data From Computer")
    return pd.read_json('./data/api_currencies/output.json')


def option3(data):
    st.session_state.messages.append("Displaying DataSet")

    st.dataframe(data)


def option4():
    st.session_state.messages.append("Option 4")


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

if st.button("Option 2"):
    st.session_state.data = option2()

if st.button("Option 3"):
    if st.session_state.data is not None:
        option3(st.session_state.data)
    else:
        st.warning("Please select an option before using Option 3.")

if st.button("Option 4"):
    option4()

indexed_messages = [f"{i + 1}: {message}" for i, message in enumerate(st.session_state.messages)]

message_text = "\n".join(indexed_messages)

st.text_area("Messages:", message_text, height=200)
