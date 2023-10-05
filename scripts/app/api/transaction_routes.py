from flask import jsonify, request
from . import api_blueprint
from ...snowflake_connection import connect_snowflake


@api_blueprint.route('/transactions', methods=['GET'])
def get_transactions():
    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM TRANSACTIONS")
        transactions = cursor.fetchall()

        return jsonify({'transactions': transactions}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@api_blueprint.route('/transaction/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM TRANSACTIONS WHERE TRANSACTION_ID = %s", (transaction_id,))
        transaction = cursor.fetchone()

        if transaction is None:
            return jsonify({'error': 'Transaction not found'}), 404

        return jsonify({'transaction': transaction}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@api_blueprint.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()

    # Basic input validation
    required_fields = ['game_id', 'turn_id','player_id', 'stock_id', 'type', 'amount_stock', 'amount_money', 'market']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required transaction data is missing'}), 400

    player_id = data['player_id']
    game_id = data['game_id']
    turn_id = data['turn_id']
    stock_id = data['stock_id']
    type_ = data['type']
    amount_stock = data['amount_stock']
    amount_money = data['amount_money']
    market = data['market']

    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO TRANSACTIONS (GAME_ID, TURN_ID,PLAYER_ID, STOCK_ID, TYPE, AMOUNT_STOCK, AMOUNT_MONEY, MARKET) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (game_id, turn_id,player_id, stock_id, type_, amount_stock, amount_money, market)
        )
        connection.commit()

        return jsonify({'message': 'Transaction created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# ... Additional routes for updating, deleting transactions