import api_connection
import datetime as dt
import pandas as pd
import credentials
import snowflake_connection as snw
import streamlit as st


def option1():
    st.session_state.messages.append("Loading Data From Internet")

    currencies = api_conection.get_currencies_names()

    params = api_conection.define_params(dt.date(2011, 1, 1), currencies)

    url = "http://api.currencylayer.com/historical"

    data = api_conection.get(url, params)

    return api_conection.format_data(data)


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

if st.button("Option 1"):
    st.session_state.data = option1()

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
