import datetime

import requests
import os
import json
import pandas as pd
import random
from credentials import credentials

def get_currencies_names(n=-1):
    # Get 
    file_path = "./data/currencies/currencies.json"
    df = pd.read_json(file_path)

    currencies_list = df['Code'].to_list()

    if n != -1:
        random_items = random.sample(currencies_list, n)
        currencies_list = random_items
    currencies = ""
    for a in currencies_list:
        currencies += a + ","

    return currencies


def define_params(date, currencies="EUR,GBP,CAD,PLN"):
    params = {

        "access_key": os.getenv('API_KEY'),
        "currencies": currencies,
        "source": "USD",
        "format": "1",
        'date': date
    }

    return params


def get(url, params, print_=False):
    # Make the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:

        data = response.json()
        # Now 'data' contains the JSON response from the API

        # json_str = response.replace("'", "''") # response.text.replace("'", "''") # Escape single quotes

        if print_:
            print(data)

        return data
    else:

        print("Request failed with status code:", response.status_code)


def format_data(initial_json_data, save_ = False):

    data_list = []

    for data in initial_json_data:
        # Create a dictionary for each item
        item_data = {
            "timestamp": data["timestamp"],
            "date": data["date"],
            **data["quotes"]
        }

        # Append the item dictionary to the list
        data_list.append(item_data)

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list)

    if save_:

        time = datetime.datetime.now()
        df.to_json(f'./data/api_currencies/{time}_output.json')

    return df
