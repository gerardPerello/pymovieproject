from ...snowflake_connection import connect_snowflake

class ForexHistory:
    def __init__(self, timestamp_id, date, currency_id, value_to_dollar):
        self.timestamp_id = timestamp_id
        self.date = date
        self.currency_id = currency_id
        self.value_to_dollar = value_to_dollar

    @classmethod
    def create(cls, data_list):

        required_fields = ['timestamp', 'date', 'currency_id', 'value_to_dollar']

        for data in data_list:
            if not all(field in data for field in required_fields):
                return {'error': 'Required currency data is missing'}

        connection = connect_snowflake()
        cursor = connection.cursor()

        try:
            query = "INSERT INTO FOREX_HISTORY (FH_timestamp_id, FH_date, FH_currency_id, FH_value_to_dollar) VALUES %s" % ', '.join(
                ['(%s, %s, %s, %s)'] * len(data_list))

            params = []
            for data in data_list:
                params.extend([data['timestamp'], data['date'], data['currency_id'], data['value_to_dollar']])

            cursor.execute(query, params)
            connection.commit()

            return {'message': 'Forex_History created successfully'}
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_timestamp_and_currency(cls, timestamp_id, currency_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM FOREX_HISTORY WHERE FH_TIMESTAMP_ID = %s AND FH_CURRENCY_ID = %s ",
                           (timestamp_id, currency_id))
            result = cursor.fetchone()
            if result:
                timestamp_id, date, currency_id, value_to_dollar = result
                return cls(timestamp_id, date, currency_id, value_to_dollar)
            else:
                return None
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_all(cls):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM FOREX_HISTORY")
            results = cursor.fetchall()
            forex_history = []
            for result in results:
                timestamp_id, date, currency_id, value_to_dollar = result
                forex_history_value = cls(timestamp_id, date, currency_id, value_to_dollar)
                forex_history.append(forex_history_value)
            return forex_history
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()
            connection.close()