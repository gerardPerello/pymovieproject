from server.app.snowflake_connection import connect_snowflake  # Your actual connection setup might be different

class Event_to_Stock:
    def __init__(self, event_id, stock_id, game_id):
        self.event_id = event_id
        self.stock_id = stock_id
        self.game_id = game_id

    @classmethod
    def create(cls, data):

        required_fields = ['stock_id', 'event_id', 'game_id']

        if not all(field in data for field in required_fields):
            return {'message': 'Required event_to_stock data is missing'}

        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            query = """INSERT INTO events_to_stocks 
                        (es_event_id, es_stock_id, es_game_id)
                       VALUES (%s, %s, %s)"""
            cursor.execute(query, (
                data['event_id'], data['stock_id'], data['game_id']
            ))
            connection.commit()
            return {'message': 'Events to Stock created successfully'}
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_id(cls, event_id, stock_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM events_to_stocks WHERE es_event_id = %s AND es_stock_id = %s",
                           (event_id, stock_id))
            result = cursor.fetchone()
            return cls(*result) if result else None
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
            cursor.execute("SELECT * FROM events_to_stocks")
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_all_by_game(cls, game_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM events_to_stocks WHERE es_game_id = %s", (game_id,))
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def update(cls, event_id, stock_id, data):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            query = """UPDATE events_to_stocks SET 
                        es_game_id = %s
                       WHERE es_event_id = %s AND es_stock_id = %s"""
            cursor.execute(query, (
                data['game_id'], event_id, stock_id
            ))
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete(cls, event_id, stock_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM events_to_stocks WHERE es_event_id = %s AND es_stock_id = %s",
                           (event_id, stock_id))
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()
