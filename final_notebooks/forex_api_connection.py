import datetime

import requests
import os
import json
import pandas as pd
import random
from client.app import controller
from credentials import credentials
from server.app.snowflake_connection import connect_snowflake

def get_currencies_names(n=-1):
    # Get from Snowflake

    connection = connect_snowflake()
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM CURRENCIES")
        results = cursor.fetchall()
        currencies = []
        for result in results:
            id, code, name, country, continent = result
            currency = cls(id, code, name, country, continent)
            currencies.append(currency)
        return currencies
    except Exception as e:
        return {'error': str(e)}
    finally:
        cursor.close()
        connection.close()


    data = [
        {
            'c_id': curr.c_id,
            'c_code': curr.c_code,
            'c_name': curr.c_name,
            'c_country': curr.c_country,
            'c_continent': curr.c_continent
        }
        for curr in currencies
    ]
    currencies_list = controller.get_all_currencies()

    currencies_info_need = {curr['c_code']:curr['c_id'] for curr in currencies_list}

    #if n != -1:
    #    random_items = random.sample(currencies_list, n)
    #    currencies_list = random_items
    currencies = ""
    for a in currencies_info_need:
        currencies += a + ","

    return currencies, currencies_info_need


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


def format_data(initial_json_data, currencies_dict, save_ = False):

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

    #We create the data for the columns we want to convert to rows.
    value_vars = ["USD"+code for code in currencies_dict.keys()]

    #We must not use this currencies because there are not data (Fuck BTC)
    not_used_vars = ['USDBTC', 'USDBYN', 'USDCLF', 'USDCUC', 'USDCUP', 'USDEEK', 'USDERN', 'USDGGP', 'USDIMP', 'USDJEP', 'USDKYD', 'USDSVC', 'USDUSD', 'USDXAG', 'USDXAU', 'USDZMW', 'USDZWL']
    for i in not_used_vars:
        value_vars.remove(i)

    #Reshape de DataFrame to get the wanted value
    df_melted = pd.melt(df, id_vars=['timestamp', 'date'], value_vars=value_vars, value_name = 'value_to_dollar')

    #We replace the CODE for the id of the currency.
    df_melted.rename(columns={'variable':'currency_id'}, inplace=True)

    currencies_dict_changed = {"USD"+code:currencies_dict[code] for code in currencies_dict.keys()}
    df_melted['currency_id'] = df_melted['currency_id'].replace(currencies_dict_changed)

    if save_:

        time = datetime.datetime.now()
        df_melted.to_json(f'./data/api_currencies/{time}_output.json')

    return df_melted
