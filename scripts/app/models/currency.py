from ...snowflake_connection import connect_snowflake


class Currency:
    def __init__(self, c_id, c_code, c_name, c_country, c_continent):
        self.c_id = c_id
        self.c_code = c_code
        self.c_name = c_name
        self.c_country = c_country
        self.c_continent = c_continent

    @classmethod
    def create(cls, data_list):
        required_fields = ['code', 'name', 'country', 'continent']

        for data in data_list:
            if not all(field in data for field in required_fields):
                return {'error': 'Required currency data is missing'}

        connection = connect_snowflake()
        cursor = connection.cursor()

        try:
            query = "INSERT INTO CURRENCIES (C_CODE, C_NAME, C_COUNTRY, C_CONTINENT) VALUES %s" % ', '.join(
                ['(%s, %s, %s, %s)'] * len(data_list))

            params = []
            for data in data_list:
                params.extend([data['code'], data['name'], data['country'], data['continent']])

            cursor.execute(query, params)
            connection.commit()

            return {'message': 'Currencies created successfully'}
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_id(cls, c_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM CURRENCY WHERE C_ID = ?", (c_id,))
            result = cursor.fetchone()
            if result:
                c_id, c_code, c_name, c_country, c_continent = result
                return cls(c_id, c_code, c_name, c_country, c_continent)
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
            cursor.execute("SELECT * FROM CURRENCY")
            results = cursor.fetchall()
            currencies = []
            for result in results:
                c_id, c_code, c_name, c_country, c_continent = result
                currency = cls(c_id, c_code, c_name, c_country, c_continent)
                currencies.append(currency)
            return currencies
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()
            connection.close()
