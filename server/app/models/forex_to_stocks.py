from server.app.snowflake_connection import connect_snowflake  # Your actual connection setup might be different


class ForexToStock:
    def __init__(self, stock_id, currency_id, currency_weight):
        self.stock_id = stock_id
        self.currency_id = currency_id
        self.currency_weight = currency_weight

    @classmethod
    def create(cls, data):

        required_fields = ['stock_id', 'currency_id', 'currency_weight']

        if not all(field in data for field in required_fields):
            return {'message': 'Required forex_to_sticks data is missing'}

        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            query = """INSERT INTO forex_to_stocks 
                        (fs_stock_id, fs_currency_id, fs_currency_weight)
                       VALUES (%s, %s, %s)"""
            cursor.execute(query, (
                data['stock_id'], data['currency_id'], data['currency_weight']
            ))
            connection.commit()
            return {'message': 'Forex To Stocks created successfully'}
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_id(cls, stock_id, currency_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM forex_to_stocks WHERE fs_stock_id = %s AND fs_currency_id = %s",
                           (stock_id, currency_id))
            result = cursor.fetchone()
            return cls(*result) if result else None
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_currency(cls, currency_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM forex_to_stocks WHERE fs_currency_id = %s",
                           (currency_id,))
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_stock(cls, stock_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM forex_to_stocks WHERE fs_stock_id = %s",
                           (stock_id,))
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
            cursor.execute("SELECT * FROM forex_to_stocks")
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def update(cls, stock_id, currency_id, data):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            query = """UPDATE forex_to_stocks SET 
                        fs_currency_weight = %s
                       WHERE fs_stock_id = %s AND fs_currency_id = %s"""
            cursor.execute(query, (
                data['currency_weight'], stock_id, currency_id
            ))
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete(cls, stock_id, currency_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM forex_to_stocks WHERE fs_stock_id = %s AND fs_currency_id = %s",
                           (stock_id, currency_id))
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()
