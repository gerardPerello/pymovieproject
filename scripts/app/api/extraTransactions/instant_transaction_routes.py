from flask import Blueprint, jsonify, request
from scripts.snowflake_connection import connect_snowflake

# Blueprint
instant_transaction_blueprint = Blueprint('instant_transaction', __name__)


# GET all instant transactions
@instant_transaction_blueprint.route('/instant_transactions', methods=['GET'])
def get_instant_transactions():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM INSTANT_TRANSACTION")
        instant_transactions = cursor.fetchall()
        return jsonify({'instant_transactions': instant_transactions}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# GET a single instant transaction by ID
@instant_transaction_blueprint.route('/instant_transaction/<int:transaction_id>', methods=['GET'])
def get_instant_transaction(transaction_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM INSTANT_TRANSACTION WHERE TRANSACTION_ID = %s", (transaction_id,))
        instant_transaction = cursor.fetchone()
        if instant_transaction is None:
            return jsonify({'error': 'Instant transaction not found'}), 404
        return jsonify({'instant_transaction': instant_transaction}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# POST a new instant transaction
@instant_transaction_blueprint.route('/instant_transaction', methods=['POST'])
def create_instant_transaction():
    data = request.get_json()
    required_fields = ['game_id', 'player_id', 'currency_id', 'amount']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required transaction data is missing'}), 400

    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO INSTANT_TRANSACTION (GAME_ID, PLAYER_ID, CURRENCY_ID, AMOUNT) 
            VALUES (%s, %s, %s, %s)
            """,
            (data['game_id'], data['player_id'], data['currency_id'], data['amount'])
        )
        connection.commit()
        return jsonify({'message': 'Instant transaction created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
