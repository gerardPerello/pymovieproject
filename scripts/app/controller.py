from .models import Currency
from .models import ForexHistory


def create_currency(data):
    message = Currency.create(data)
    return message


def create_forex_history(data):
    message = ForexHistory.create(data)
    return message

def get_all_currencies():
    currencies = Currency.get_all()
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
    return data
