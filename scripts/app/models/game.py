class Game:
    def __init__(self, game_id, game_name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count):
        self.game_id = game_id
        self.game_name = game_name
        self.total_turns = total_turns
        self.sec_per_turn = sec_per_turn
        self.starting_money = starting_money
        self.turns_between_events = turns_between_events
        self.player_count = player_count
        self.stock_count = stock_count

    def create(self):
        # Logic to create a new game in the database using Snowflake connection
        pass

    @classmethod
    def get_by_id(cls, game_id):
        # Logic to get a game by id using Snowflake connection
        pass