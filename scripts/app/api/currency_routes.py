from flask import Blueprint, jsonify, request
from ...snowflake_connection import connect_snowflake

# Blueprint
currency_blueprint = Blueprint('currency', __name__)


# GET all currencies
@currency_blueprint.route('/currencies', methods=['GET'])
def get_currencies():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM CURRENCY")
        currencies = cursor.fetchall()
        return jsonify({'currencies': currencies}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# GET a single currency by ID
@currency_blueprint.route('/currency/<int:currency_id>', methods=['GET'])
def get_currency(currency_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM CURRENCY WHERE CURRENCY_ID = %s", (currency_id,))
        currency = cursor.fetchone()
        if currency is None:
            return jsonify({'error': 'Currency not found'}), 404
        return jsonify({'currency': currency}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# POST a new currency
@currency_blueprint.route('/currency', methods=['POST'])
def create_currency():
    data = request.get_json()
    required_fields = ['currency_name', 'currency_country', 'currency_continent']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required currency data is missing'}), 400

    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO CURRENCY (CURRENCY_NAME, CURRENCY_COUNTRY, CURRENCY_CONTINENT) VALUES (%s, %s, %s)",
            (data['currency_name'], data['currency_country'], data['currency_continent'])
        )
        connection.commit()
        return jsonify({'message': 'Currency created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
