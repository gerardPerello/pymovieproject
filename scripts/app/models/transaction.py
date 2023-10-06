from ...snowflake_connection import connect_snowflake  # Your actual connection setup might be different

class Transaction:
    def __init__(self, transaction_id, player_id, game_id, turn_id, stock_id, type_, amount_stock, amount_money,
                 market):
        self.id = transaction_id
        self.player_id = player_id
        self.game_id = game_id
        self.turn_id = turn_id
        self.stock_id = stock_id
        self.type = type_
        self.amount_stock = amount_stock
        self.amount_money = amount_money
        self.market = market

    @classmethod
    def create(cls, data):
        # Note: Make sure to validate 'data' before executing query to prevent SQL injection
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            query = """INSERT INTO transactions 
                        (t_game_id, t_turn_id, t_player_id, t_stock_id, t_type, t_stock_amount, t_money_amount, t_with_market) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                data['game_id'], data['turn_id'], data['player_id'], data['stock_id'],
                data['type'], data['amount_stock'], data['amount_money'], data['market']
            ))
            connection.commit()
            return {'message': 'Transaction created successfully'}
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_id(cls, transaction_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM transactions WHERE t_id = %s", (transaction_id,))
            result = cursor.fetchone()
            return cls(*result) if result else None
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_player(cls, player_id, game_id, turn_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM transactions WHERE t_player_id = %s AND t_game_id = %s AND t_turn_id = %s",
                (player_id, game_id, turn_id)
            )
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_sells_or_buys(cls, game_id, turn_id, type_):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM transactions WHERE t_game_id = %s AND t_turn_id = %s AND t_type = %s",
                (game_id, turn_id, type_)
            )
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
            cursor.execute("SELECT * FROM transactions")
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def update(cls, transaction_id, data):
        # Ensure to validate 'data' before query execution
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            query = """UPDATE transactions SET 
                        t_game_id = %s, 
                        t_turn_id = %s, 
                        t_player_id = %s, 
                        t_stock_id = %s, 
                        t_type = %s, 
                        t_stock_amount = %s, 
                        t_money_amount = %s, 
                        t_with_market = %s 
                       WHERE t_id = %s"""
            cursor.execute(query, (
                data['game_id'], data['turn_id'], data['player_id'], data['stock_id'],
                data['type'], data['amount_stock'], data['amount_money'], data['market'], transaction_id
            ))
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete(cls, transaction_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM transactions WHERE t_id = %s", (transaction_id,))
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()
