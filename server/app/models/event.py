from server.app.snowflake_connection import connect_snowflake  # Your actual connection setup might be different


class Event:
    def __init__(self, event_id, type_event, content_event, percentage_or_total, percentage_change, total_change):
        self.event_id = event_id
        self.type_event = type_event
        self.content_event = content_event
        self.percentage_or_total = percentage_or_total
        self.percentage_change = percentage_change
        self.total_change = total_change

    @classmethod
    def create(cls, data):

        required_fields = ['event_id', 'type_event', 'content_event', 'percentage_or_total', 'percentage_change', 'total_change']

        if not all(field in data for field in required_fields):
            return {'message': 'Required game data is missing'}

        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            query = """INSERT INTO events 
                        (e_type, e_content, e_pct_or_total, e_pct_change, e_total_change)
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                data['type_event'], data['content_event'], data['percentage_or_total'],
                data['percentage_change'], data['total_change']
            ))
            connection.commit()
            return {'message': 'Events created successfully'}
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_id(cls, event_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM events WHERE e_id = %s", (event_id,))
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
            cursor.execute("SELECT * FROM events")
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_by_type(cls, type_event):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM events WHERE e_type = %s", (type_event,))
            results = cursor.fetchall()
            return [cls(*result) for result in results]
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def update(cls, event_id, data):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            query = """UPDATE events SET 
                        e_type = %s,
                        e_content = %s,
                        e_pct_or_total = %s,
                        e_pct_change = %s,
                        e_total_change = %s
                       WHERE e_id = %s"""
            cursor.execute(query, (
                data['type_event'], data['content_event'], data['percentage_or_total'],
                data['percentage_change'], data['total_change'], event_id
            ))
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete(cls, event_id):
        connection = connect_snowflake()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM events WHERE e_id = %s", (event_id,))
            connection.commit()
        except Exception as e:
            return {'message': str(e)}
        finally:
            cursor.close()
            connection.close()
