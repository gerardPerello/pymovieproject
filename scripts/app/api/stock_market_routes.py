from flask import Blueprint, jsonify, request
from ...snowflake_connection import connect_snowflake

# Blueprint
stock_market_blueprint = Blueprint('stock_market', __name__)

# GET all stock market entries
@stock_market_blueprint.route('/stock_markets', methods=['GET'])
def get_stock_markets():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM STOCK_MARKET")
        stock_markets = cursor.fetchall()
        return jsonify({'stock_markets': stock_markets}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# GET a single stock market entry by IDs
@stock_market_blueprint.route('/stock_market/<int:stock_id>/<int:game_id>/<int:turn_id>', methods=['GET'])
def get_stock_market(stock_id, game_id, turn_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM STOCK_MARKET WHERE STOCK_ID = %s AND GAME_ID = %s AND TURN_ID = %s",
            (stock_id, game_id, turn_id,)
        )
        stock_market = cursor.fetchone()
        if stock_market is None:
            return jsonify({'error': 'Stock Market entry not found'}), 404
        return jsonify({'stock_market': stock_market}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# POST a new stock market entry
@stock_market_blueprint.route('/stock_market', methods=['POST'])
def create_stock_market():
    data = request.get_json()
    required_fields = ['stock_id', 'game_id', 'turn_id', 'stock_value']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required stock market data is missing'}), 400

    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO STOCK_MARKET (STOCK_ID, GAME_ID, TURN_ID, STOCK_VALUE) VALUES (%s, %s, %s, %s)",
            (data['stock_id'], data['game_id'], data['turn_id'], data['stock_value'])
        )
        connection.commit()
        return jsonify({'message': 'Stock Market entry created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
