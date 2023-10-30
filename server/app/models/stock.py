from ..snowflake_connection import connect_snowflake

class Stock:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):



        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO STOCKS (s_name) VALUES (%s)",
                (name)
            )
            connection.commit()
            cursor.execute("SELECT * FROM STOCKS WHERE s_name = %s", (name,))
            result = cursor.fetchone()
            if result:
                id, name = result
                return cls(id, name)
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete(cls, id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM STOCKS WHERE s_id = %s", (id,))
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def update(cls, id, name):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE STOCKS SET s_name = %s WHERE s_id = %s",
                (name, id)
            )
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_from_id(cls, id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM STOCKS WHERE s_id = %s", (id,))
            result = cursor.fetchone()
            if result:
                return cls(*result)
            return None
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
            cursor.execute("SELECT * FROM STOCKS")
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()
