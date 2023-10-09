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


@currency_blueprint.route('/currency', methods=['POST'])
def create():
    data = request.get_json()
    required_fields = ['code', 'name', 'country', 'continent']

    if not all(field in data for field in required_fields):
        return {'error': 'Required currency data is missing'}

    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        query = "INSERT INTO CURRENCIES (C_CODE, C_NAME, C_COUNTRY, C_CONTINENT) VALUES %s" % ', '.join(
            ['(%s, %s, %s, %s)'])

        params = []
        params.extend([data['code'], data['name'], data['country'], data['continent']])

        cursor.execute(query, params)
        connection.commit()

        return jsonify({'message': 'Currency created successfully'}), 201
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
