from ..snowflake_connection import connect_snowflake

class StockMarket:
    def __init__(self, stock_id, game_id, turn_id, stock_value):
        self.stock_id = stock_id
        self.game_id = game_id
        self.turn_id = turn_id
        self.stock_value = stock_value

    @classmethod
    def create(cls, stock_id, game_id, turn_id, stock_value):


        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO STOCK_MARKET (sm_stock_id, sm_game_id, sm_turn_id, sm_stock_value) VALUES (%s, %s, %s, %s)",
                (stock_id, game_id, turn_id, stock_value)
            )
            connection.commit()
            return {'message': 'StockMarket created successfully'}
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_id(cls, stock_id, game_id, turn_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM STOCK_MARKET WHERE sm_stock_id = %s AND sm_game_id = %s AND sm_turn_id = %s",
                           (stock_id, game_id, turn_id))
            result = cursor.fetchone()
            if result:
                return cls(*result)
            return None
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    # Your other methods would follow a similar pattern, adjusting the SQL queries as needed.

    # Example for one more method:
    @classmethod
    def get_stock_by_game(cls, stock_id, game_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM STOCK_MARKET WHERE sm_stock_id = %s AND sm_game_id = %s",
                           (stock_id, game_id))
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
            cursor.execute("SELECT * FROM STOCK_MARKET WHERE sm_game_id = %s", (game_id,))
            results = cursor.fetchall()
            return [cls(*result) for result in results]
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
            cursor.execute("SELECT * FROM STOCK_MARKET")
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_turn(cls, game_id, turn_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM STOCK_MARKET WHERE sm_game_id = %s AND sm_turn_id = %s",
                           (game_id, turn_id))
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete(cls, stock_id, game_id, turn_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM STOCK_MARKET WHERE sm_stock_id = %s AND sm_game_id = %s AND sm_turn_id = %s",
                (stock_id, game_id, turn_id)
            )
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def update(cls, stock_id, game_id, turn_id, stock_value):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE STOCK_MARKET SET STOCK_VALUE = %s WHERE sm_stock_id = %s AND sm_game_id = %s AND sm_turn_id = "
                "%s",
                (stock_value, stock_id, game_id, turn_id)
            )
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()