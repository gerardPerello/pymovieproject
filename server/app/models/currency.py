from ..snowflake_connection import connect_snowflake


class Currency:
    def __init__(self, id, code, name, country, continent):
        self.id = id
        self.code = code
        self.name = name
        self.country = country
        self.continent = continent

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
    def get_by_id(cls, id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM CURRENCIES WHERE C_ID = %s", (id,))
            result = cursor.fetchone()
            if result:
                id, code, name, country, continent = result
                return cls(id, code, name, country, continent)
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
            cursor.execute("SELECT * FROM CURRENCIES")
            results = cursor.fetchall()
            currencies = []
            for result in results:
                id, code, name, country, continent = result
                currency = cls(id, code, name, country, continent)
                currencies.append(currency)
            return currencies
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()
            connection.close()
