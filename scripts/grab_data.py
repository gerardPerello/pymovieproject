import requests
import json
import datetime as dt
import pandas as pd
from time import sleep
import os
import sys
sys.path.append('../scripts/credentials')

import credentials
# Get 
file_path = '../data/currencies.json'
df = pd.read_json(file_path)

currencies = ""
for a in df['Code'].values:
    currencies += a + ","

#test


url = 'http://api.currencylayer.com/historical'

start_date = dt.date(2011, 1, 1)
end_date = dt.date(2011, 1, 2)
delta = dt.timedelta(days=1)

data = []
while start_date <= end_date:
    print(start_date)
    
    params = {
        'access_key' : os.getenv('API_KEY'),
        'source' : 'USD',
        'currencies' : currencies,
        'date' : start_date
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        json_data = response.json()
        data.append(json_data)
    else:
        print('Error connecting to the API.')
        print(response)

    start_date += delta

    sleep(1)

print(pd.json_normalize(data))