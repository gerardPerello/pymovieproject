from server.app.snowflake_connection import connect_snowflake

class PlayersToGame:
    def __init__(self, game_id, player_id, turn_id, amount_of_money):
        self.game_id = game_id
        self.player_id = player_id
        self.turn_id = turn_id
        self.amount_of_money = amount_of_money

    @classmethod
    def create(cls, game_id, player_id, turn_id, amount_of_money):

        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO PLAYERS_TO_GAME (ptg_player_id,ptg_game_id, ptg_turn_id, ptg_money_amount) VALUES (%s, "
                "%s, %s, %s)",
                (player_id, game_id, turn_id, amount_of_money)
            )

            connection.commit()
            
            return {'message': 'Player_To_Game created successfully'}
        except Exception as e:
            return{"message": str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_id(cls, game_id, player_id, turn_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM PLAYERS_TO_GAME WHERE ptg_game_id = %s AND ptg_player_id = %s AND ptg_turn_id = %s",
                (game_id, player_id, turn_id)
            )
            result = cursor.fetchone()
            if result:
                return cls(*result)
            return None
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_all_by_player_in_game(cls, game_id, player_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM PLAYERS_TO_GAME WHERE ptg_game_id = %s AND ptg_player_id = %s",
                (game_id, player_id)
            )
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete(cls, game_id, player_id, turn_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM PLAYERS_TO_GAME WHERE ptg_game_id = %s AND ptg_player_id = %s AND ptg_turn_id = %s",
                (game_id, player_id, turn_id)
            )
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def update(cls, game_id, player_id, turn_id, amount_of_money):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE PLAYERS_TO_GAME SET ptg_money_amount = %s WHERE ptg_game_id = %s AND ptg_player_id = %s AND ptg_turn_id = %s",
                (amount_of_money, game_id, player_id, turn_id)
            )
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()
