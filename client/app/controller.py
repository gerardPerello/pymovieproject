from .models import *


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


def create_game(name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count):
    message = Game.create(name, total_turns, sec_per_turn, starting_money,
                          turns_between_events, player_count, stock_count)
    return message

def get_name(name):
    name = Game.get_by_name(name)
    return name

def create_player(data, dataPlayerToGame):
    message = Player.create(data)
    message = PlayersToGame.create(dataPlayerToGame)