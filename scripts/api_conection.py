import requests
import os

# Define the API URL
url = "http://apilayer.net/api/live"
params = dict()

def define_params(currencies = "EUR,GBP,CAD,PLN"):
    params = {
        "access_key": os.getenv("API_KEY"),
        "currencies": currencies,
        "source": "USD",
        "format": "1"
    }

def get(url, params, print_ = False):
    # Make the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        
        data = response.json()
        # Now 'data' contains the JSON response from the API
        
        json_str = response.replace("'", "''") # response.text.replace("'", "''") # Escape single quotes 

        if print_:
            print(data)

        return data
    else:
        
        print("Request failed with status code:", response.status_code)
    