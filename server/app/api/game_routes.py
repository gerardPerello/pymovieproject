from flask import Blueprint, jsonify, request
from ..snowflake_connection import connect_snowflake
# Blueprint
game_blueprint = Blueprint('game', __name__)


@game_blueprint.route('/game', methods=['POST'])
def create():
    data = request.get_json()
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO GAMES (
                g_name, g_total_turns, g_sec_per_turn, g_starting_money, 
                g_turns_between_events, g_player_count, g_stocks_count
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (data['name'], data['total_turns'], data['sec_per_turn'], data['starting_money'],
              data['turns_between_events'], data['player_count'], data['stock_count']))
        connection.commit()
        return {'message': 'Game created successfully'}
    except Exception as e:
        return {'message': str(e)}
    finally:
        cursor.close()
        connection.close()


@game_blueprint.route('/game', methods=['GET'])
def get_all():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM GAMES")
        results = cursor.fetchall()
        return jsonify({'games': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@game_blueprint.route('/game/<string:game_name>', methods=['GET'])
def get_by_name(game_name):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM GAMES WHERE g_name = %s", (game_name,))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'error': 'game not found'}), 404
        return jsonify({'game': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@game_blueprint.route('/game/<int:game_id>', methods=['PUT'])
def update(game_id):
    new_data = request.get_json()
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            UPDATE GAMES SET 
                g_name = %s,
                g_total_turns = %s,
                g_sec_per_turn = %s,
                g_starting_money = %s,
                g_turns_between_events = %s,
                g_player_count = %s,
                g_stocks_count = %s
            WHERE g_id = %s
        """, (new_data['name'], new_data['total_turns'], new_data['sec_per_turn'],
              new_data['starting_money'], new_data['turns_between_events'],
              new_data['player_count'], new_data['stock_count'], game_id))
        connection.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Game updated successfully'}), 201
        else:
            return jsonify({'message': 'Game not found'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
