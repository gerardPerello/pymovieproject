from flask import Blueprint, jsonify, request
from ..snowflake_connection import connect_snowflake

# Blueprint
transaction_blueprint = Blueprint('transaction', __name__)


@transaction_blueprint.route('/transactions', methods=['GET'])
def create():
    data = request.get_json()

    required_fields = ['game_id', 'turn_id', 'player_id', 'stock_id',
                       'amount_stock', 'amount_money', 'market', 'type']

    if not all(field in data for field in required_fields):
        return {'message': 'Required transaction data is missing'}

    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        query = """INSERT INTO transactions 
                            (t_game_id, t_turn_id, t_player_id, t_stock_id, t_type, t_stock_amount, t_money_amount, t_with_market) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        results = cursor.execute(query, (
            data['game_id'], data['turn_id'], data['player_id'], data['stock_id'],
            data['type'], data['amount_stock'], data['amount_money'], data['market']
        ))
        connection.commit()
        return jsonify({'transactions': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
