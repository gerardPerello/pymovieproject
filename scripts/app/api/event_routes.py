from flask import jsonify, request, Blueprint
from ...snowflake_connection import connect_snowflake

event_blueprint = Blueprint('event', __name__)

@event_blueprint.route('/events', methods=['GET'])
def get_events():
    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM EVENTS")
        events = cursor.fetchall()

        return jsonify({'events': events}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@event_blueprint.route('/event/<int:event_id>', methods=['GET'])
def get_event(event_id):
    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM EVENTS WHERE EVENT_ID = %s", (event_id,))
        event = cursor.fetchone()

        if event is None:
            return jsonify({'error': 'Event not found'}), 404

        return jsonify({'event': event}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@event_blueprint.route('/event', methods=['POST'])
def create_event():
    data = request.get_json()

    required_fields = ['type_event', 'content_event', 'percentage_or_total', 'percentage_change', 'total_change']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required event data is missing'}), 400

    type_event = data['type_event']
    content_event = data['content_event']
    percentage_or_total = data['percentage_or_total']
    percentage_change = data['percentage_change']
    total_change = data['total_change']

    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """INSERT INTO EVENTS (TYPE_EVENT, CONTENT_EVENT, PERCENTAGE_OR_TOTAL, PERCENTAGE_CHANGE, TOTAL_CHANGE) 
               VALUES (%s, %s, %s, %s, %s)""",
            (type_event, content_event, percentage_or_total, percentage_change, total_change)
        )
        connection.commit()

        return jsonify({'message': 'Event created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()