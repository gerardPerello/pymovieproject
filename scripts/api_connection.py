import requests
import os
import json
import pandas as pd
from credentials import credentials

def get_currencies_names(n=-1):
    # Get 
    file_path = "./data/currencies/currencies.json"
    df = pd.read_json(file_path)

    currencies = ""
    for a in df['Code'].values:
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
    df = pd.DataFrame({
        "timestamp": [initial_json_data["timestamp"]],
        "date": [initial_json_data["date"]],
        **initial_json_data["quotes"]
    })

    if save_:
        df.to_json('output.json')

    return df
