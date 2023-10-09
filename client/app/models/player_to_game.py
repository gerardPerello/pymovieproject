from client.app.snowflake_connection import connect_snowflake

class PlayersToGame:
    def __init__(self, game_id, player_id, turn_id, amount_of_money):
        self.game_id = game_id
        self.player_id = player_id
        self.turn_id = turn_id
        self.amount_of_money = amount_of_money

