from flask import Blueprint, jsonify, request
from ..snowflake_connection import connect_snowflake
# Blueprint
currency_blueprint = Blueprint('currency', __name__)


# GET all currencies
@currency_blueprint.route('/currencies', methods=['GET'])
def get_all():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM CURRENCIES")
        results = cursor.fetchall()
        return jsonify({'currencies': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# GET a single currency by ID
@currency_blueprint.route('/currency/<int:currency_id>', methods=['GET'])
def get_by_id(currency_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM CURRENCIES WHERE C_ID = %s", (currency_id,))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'error': 'Currency not found'}), 404
        return jsonify({'currency': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
