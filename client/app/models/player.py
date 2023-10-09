from client.app.snowflake_connection import connect_snowflake

class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, data):
        required_fields = ['name']

        if not all(field in data for field in required_fields):
            return {'message': 'Required player data is missing'}

        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO PLAYERS (
                    pl_name
                ) VALUES (%s)
            """, (data['name']))
            connection.commit()
            return {'message': 'Player created successfully'}
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
            cursor.execute("SELECT * FROM PLAYERS")
            results = cursor.fetchall()
            players = []
            for result in results:
                id,name = result
                player = cls(id,name)
                players.append(player)
            return players
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_id(cls, player_id):
        pass

    @classmethod
    def delete(cls, player_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM PLAYERS WHERE pl_id = %s", (player_id,))
            connection.commit()
            if cursor.rowcount > 0:
                return {'message': 'Player deleted successfully'}
            else:
                return {'message': 'Player not found'}
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def update(cls, player_id, new_data):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE PLAYERS SET 
                    pl_name = %s
                WHERE pl_id = %s
            """, (new_data['name'], player_id))
            connection.commit()
            if cursor.rowcount > 0:
                return {'message': 'Player updated successfully'}
            else:
                return {'message': 'Player not found'}
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()
            connection.close()
