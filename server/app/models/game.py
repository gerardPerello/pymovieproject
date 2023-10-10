from server.app.snowflake_connection import connect_snowflake


class Game:
    def __init__(self, id, name, total_turns, sec_per_turn, starting_money,
                 turns_between_events, player_count, stock_count, open_):
        self.id = id
        self.name = name
        self.total_turns = total_turns
        self.sec_per_turn = sec_per_turn
        self.starting_money = starting_money
        self.turns_between_events = turns_between_events
        self.player_count = player_count
        self.stock_count = stock_count
        self.open_ = open_


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'total_turns': self.total_turns,
            'sec_per_turn': self.sec_per_turn,
            'starting_money': self.starting_money,
            'turns_between_events': self.turns_between_events,
            'player_count': self.player_count,
            'stock_count': self.stock_count,

        }

    @classmethod
    def create(cls, name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count):


        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO GAMES (
                    g_name, g_total_turns, g_sec_per_turn, g_starting_money, 
                    g_turns_between_events, g_player_count, g_stocks_count
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count))
            connection.commit()
            return {'message': 'Game created successfully'}
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_all(cls):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM GAMES WHERE g_is_open = True")
            results = cursor.fetchall()
            games = []
            for result in results:
                id, name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count, open_ = result
                game = cls(id, name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count,
                           stock_count, open_)
                games.append(game)
            return games
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_id(cls, game_name):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM GAMES WHERE g_id = %s", (game_name,))
            result = cursor.fetchone()
            if result:
                id, name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count, open_ = result
                return cls(id, name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count,
                           stock_count, open_)
            else:
                return None
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete(cls, game_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM GAMES WHERE g_id = %s", (game_id,))
            connection.commit()
            if cursor.rowcount > 0:
                return {'message': 'Game deleted successfully'}
            else:
                return {'message': 'Game not found'}
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def update(cls, game_id, new_data):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE GAMES SET 
                    g_name = %s,
                    g_total_turns = %s,
                    g_sec_per_turn = %s,
                    g_starting_money = %s,
                    g_turns_between_events = %s,
                    g_player_count = %s,
                    g_stocks_count = %s
                WHERE g_id = %s
            """, (new_data['name'], new_data['total_turns'], new_data['sec_per_turn'],
                  new_data['starting_money'], new_data['turns_between_events'],
                  new_data['player_count'], new_data['stock_count'], game_id))
            connection.commit()
            if cursor.rowcount > 0:
                return {'message': 'Game updated successfully'}
            else:
                return {'message': 'Game not found'}
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()
