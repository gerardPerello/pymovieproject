from flask import Blueprint, jsonify, request
from ...snowflake_connection import connect_snowflake

# Blueprint
forex_history_blueprint = Blueprint('forex_history', __name__)

# GET all forex history entries
@forex_history_blueprint.route('/forex_histories', methods=['GET'])
def get_forex_histories():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM FOREX_HISTORY")
        forex_histories = cursor.fetchall()
        return jsonify({'forex_histories': forex_histories}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# GET a single forex history entry by ID
@forex_history_blueprint.route('/forex_history/<int:timestamp_id>', methods=['GET'])
def get_forex_history(timestamp_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM FOREX_HISTORY WHERE TIMESTAMP_ID = %s", (timestamp_id,))
        forex_history = cursor.fetchone()
        if forex_history is None:
            return jsonify({'error': 'Forex History entry not found'}), 404
        return jsonify({'forex_history': forex_history}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# POST a new forex history entry
@forex_history_blueprint.route('/forex_history', methods=['POST'])
def create_forex_history():
    data = request.get_json()
    required_fields = ['timestamp_id', 'date', 'currency_id', 'value_to_dollar']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required forex history data is missing'}), 400

    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO FOREX_HISTORY (TIMESTAMP_ID, DATE, CURRENCY_ID, VALUE_TO_DOLLAR) VALUES (%s, %s, %s, %s)",
            (data['timestamp_id'], data['date'], data['currency_id'], data['value_to_dollar'])
        )
        connection.commit()
        return jsonify({'message': 'Forex History entry created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
