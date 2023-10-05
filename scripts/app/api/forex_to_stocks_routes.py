from flask import Blueprint, jsonify, request
from ...snowflake_connection import connect_snowflake

# Blueprint
forex_to_stocks_blueprint = Blueprint('forex_to_stocks', __name__)


# GET all ForexToStock relations
@forex_to_stocks_blueprint.route('/forex_to_stocks', methods=['GET'])
def get_forex_to_stocks():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM FOREX_TO_STOCKS")
        forex_to_stocks = cursor.fetchall()
        return jsonify({'forex_to_stocks': forex_to_stocks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# GET a single ForexToStock relation by stock_id and currency_id
@forex_to_stocks_blueprint.route('/forex_to_stock/<int:stock_id>/<int:currency_id>', methods=['GET'])
def get_forex_to_stock(stock_id, currency_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM FOREX_TO_STOCKS WHERE STOCK_ID = %s AND CURRENCY_ID = %s", (stock_id, currency_id,))
        forex_to_stock = cursor.fetchone()
        if forex_to_stock is None:
            return jsonify({'error': 'ForexToStock relation not found'}), 404
        return jsonify({'forex_to_stock': forex_to_stock}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# POST a new ForexToStock relation
@forex_to_stocks_blueprint.route('/forex_to_stock', methods=['POST'])
def create_forex_to_stock():
    data = request.get_json()
    required_fields = ['stock_id', 'currency_id', 'currency_weight']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required ForexToStock data is missing'}), 400

    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO FOREX_TO_STOCKS (STOCK_ID, CURRENCY_ID, CURRENCY_WEIGHT) VALUES (%s, %s, %s)",
            (data['stock_id'], data['currency_id'], data['currency_weight'])
        )
        connection.commit()
        return jsonify({'message': 'ForexToStock relation created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
