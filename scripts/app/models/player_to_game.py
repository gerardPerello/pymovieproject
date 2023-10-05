class PlayersToGame:
    def __init__(self, game_id, player_id, color_id, team_id):
        self.game_id = game_id
        self.player_id = player_id
        self.color_id = color_id
        self.team_id = team_id

    def create(self):
        pass

    @classmethod
    def get_by_id(cls, game_id, player_id):
        pass