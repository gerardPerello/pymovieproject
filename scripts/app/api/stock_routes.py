from flask import Blueprint, jsonify, request
from ...snowflake_connection import connect_snowflake

# Blueprint
stock_blueprint = Blueprint('stock', __name__)

# GET all stocks
@stock_blueprint.route('/stocks', methods=['GET'])
def get_stocks():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM STOCKS")
        stocks = cursor.fetchall()
        return jsonify({'stocks': stocks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# GET a single stock by ID
@stock_blueprint.route('/stock/<int:stock_id>', methods=['GET'])
def get_stock(stock_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM STOCKS WHERE STOCK_ID = %s", (stock_id,))
        stock = cursor.fetchone()
        if stock is None:
            return jsonify({'error': 'Stock not found'}), 404
        return jsonify({'stock': stock}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# POST a new stock
@stock_blueprint.route('/stock', methods=['POST'])
def create_stock():
    data = request.get_json()
    required_fields = ['name']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required stock data is missing'}), 400

    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO STOCKS (NAME) VALUES (%s)",
            (data['name'],)
        )
        connection.commit()
        return jsonify({'message': 'Stock created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
