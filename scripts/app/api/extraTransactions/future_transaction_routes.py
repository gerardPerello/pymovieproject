from flask import Blueprint, jsonify, request
from scripts.snowflake_connection import connect_snowflake

# Blueprint
future_transaction_blueprint = Blueprint('future_transaction', __name__)


# GET all future transactions
@future_transaction_blueprint.route('/future_transactions', methods=['GET'])
def get_future_transactions():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM FUTURE_TRANSACTION")
        future_transactions = cursor.fetchall()
        return jsonify({'future_transactions': future_transactions}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# GET a single future transaction by ID
@future_transaction_blueprint.route('/future_transaction/<int:transaction_id>', methods=['GET'])
def get_future_transaction(transaction_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM FUTURE_TRANSACTION WHERE TRANSACTION_ID = %s", (transaction_id,))
        future_transaction = cursor.fetchone()
        if future_transaction is None:
            return jsonify({'error': 'Future transaction not found'}), 404
        return jsonify({'future_transaction': future_transaction}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# POST a new future transaction
@future_transaction_blueprint.route('/future_transaction', methods=['POST'])
def create_future_transaction():
    data = request.get_json()
    required_fields = ['game_id', 'player_id', 'currency_id', 'amount', 'future_price']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required transaction data is missing'}), 400

    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO FUTURE_TRANSACTION (GAME_ID, PLAYER_ID, CURRENCY_ID, AMOUNT, FUTURE_PRICE) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (data['game_id'], data['player_id'], data['currency_id'], data['amount'], data['future_price'])
        )
        connection.commit()
        return jsonify({'message': 'Future transaction created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
