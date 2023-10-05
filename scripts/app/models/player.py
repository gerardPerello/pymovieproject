class Player:
    def __init__(self, player_id, player_name, player_email, player_pass):
        self.player_id = player_id
        self.player_name = player_name
        self.player_email = player_email
        self.player_pass = player_pass

    def create(self):
        # Logic to create a new player in the database using Snowflake connection
        pass

    @classmethod
    def get_by_id(cls, player_id):
        # Logic to get a player by id using Snowflake connection
        pass