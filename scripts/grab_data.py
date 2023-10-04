import requests
import json
import datetime as dt
import pandas as pd
from time import sleep

# Get 
html_file_path = 'C:/Users/edrae/Downloads/cl-currencies-table.html'
df = pd.read_html(html_file_path)[0]

currencies = ""
for a in df['Code'].values:
    currencies += a + ","

#test

my_api_key = '0b1558630f3f8beb22e890609d581131'

url = 'http://api.currencylayer.com/historical'

start_date = dt.date(2011, 1, 1)
end_date = dt.date(2011, 1, 2)
delta = dt.timedelta(days=1)

data = []
while start_date <= end_date:
    print(start_date)
    
    params = {
        'access_key' : my_api_key,
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

pd.json_normalize(data)