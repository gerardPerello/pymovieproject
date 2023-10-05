from flask import Blueprint, jsonify, request
from ...snowflake_connection import connect_snowflake

event_to_stock_blueprint = Blueprint('event_to_stock', __name__)

@event_to_stock_blueprint.route('/event_to_stock', methods=['GET'])
def get_event_to_stocks():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM event_to_stock")
        results = cursor.fetchall()
        return jsonify({'event_to_stock': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@event_to_stock_blueprint.route('/event_to_stock/<int:id>', methods=['GET'])
def get_event_to_stock(id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM event_to_stock WHERE ID = %s", (id,))
        result = cursor.fetchone()
        return jsonify({'event_to_stock': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@event_to_stock_blueprint.route('/event_to_stock', methods=['POST'])
def create_event_to_stock():
    data = request.get_json()
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        # Add the insertion logic here
        # cursor.execute(INSERTION_QUERY, (data['field1'], data['field2'], ...))
        connection.commit()
        return jsonify({'message': 'Event_to_Stock created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
