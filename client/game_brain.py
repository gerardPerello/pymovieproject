from .app.models import *
from .app import controller
class GameBrain:
    def __init__(self, name, total_turns, sec_per_turn, starting_money,
                 turns_between_events, player_count, stock_count):
        self.game = None
        self.turn = 0
        self.player = None
        self.players = []
        self.stocks = []
        self.currencies = []
        self.create_and_push_game(name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count)


    def create_and_push_game(self, name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count):
        #self.game = Game(*data)
        #Convert game to data
        #data = game.to_dict()
        message = controller.create_game(name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count)
        self.game = controller.get_name(name)

    def join_game(self, gameName, playerName):
        self.game = controller.get_name(gameName)
        self.player = controller.create_player()

    def change_turn(self):
        pass

    def push_actual_player(self,data):
        message = controller.create_player(data)

