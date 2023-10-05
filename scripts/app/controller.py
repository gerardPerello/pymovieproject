from .models import Currency


def create_currency(data):
    message = Currency.create(data)
    return message