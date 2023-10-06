from ...snowflake_connection import connect_snowflake  # Your actual connection setup might be different

class Portfolio:
    def __init__(self, player_id, game_id, turn_id, stock_id, amount):
        self.player_id = player_id
        self.game_id = game_id
        self.stock_id = stock_id
        self.turn_id = turn_id
        self.amount = amount

    @classmethod
    def create(cls, player_id, game_id, turn_id, stock_id, amount):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO PORTFOLIO (po_player_id, po_game_id, po_stock_id, po_turn_id, po_amount) VALUES (%s, %s, %s, %s, %s)",
                (player_id, game_id, stock_id, turn_id, amount)
            )
            connection.commit()
            return {'message': 'Portfolio created successfully'}
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_id(cls, player_id, game_id, stock_id, turn_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM PORTFOLIO WHERE po_player_id = %s AND po_game_id = %s AND po_stock_id = %s AND po_turn_id = %s",
                (player_id, game_id, stock_id, turn_id)
            )
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
                "SELECT * FROM PORTFOLIO WHERE po_player_id = %s AND po_game_id = %s AND po_turn_id = %s",
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
    def get_by_turn(cls, game_id, turn_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM PORTFOLIO WHERE po_game_id = %s AND po_turn_id = %s",
                (game_id, turn_id)
            )
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_stock(cls, stock_id, game_id, turn_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT * FROM PORTFOLIO WHERE po_stock_id = %s AND po_game_id = %s AND po_turn_id = %s",
                (stock_id, game_id, turn_id)
            )
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def update(cls, player_id, game_id, turn_id, stock_id, new_amount):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE PORTFOLIO SET po_amount = %s WHERE po_player_id = %s AND po_game_id = %s AND po_stock_id = %s AND po_turn_id = %s",
                (new_amount, player_id, game_id, stock_id, turn_id)
            )
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete(cls, player_id, game_id, stock_id, turn_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM PORTFOLIO WHERE po_player_id = %s AND po_game_id = %s AND po_stock_id = %s AND po_turn_id = %s",
                (player_id, game_id, stock_id, turn_id)
            )
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()