from flask import Blueprint, jsonify, request
from ..snowflake_connection import connect_snowflake
from ..logic import gameBrains
from ..logic import GameBrain
from ..models import Game
from ..sockets.events import handle_next_turn
# Blueprint
import json

game_blueprint = Blueprint('game', __name__)


@game_blueprint.route('/game', methods=['POST'])
def create():
    data = request.get_json()
    print(data)
    print(data['name'])
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        result = cursor.execute("""
            INSERT INTO GAMES (
                g_name, g_total_turns, g_sec_per_turn, g_starting_money, 
                g_turns_between_events, g_player_count, g_stocks_count, g_is_open
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (data['name'], data['total_turns'], data['sec_per_turn'], data['starting_money'],
              data['turns_between_events'], data['player_count'], data['stock_count'], True))
        connection.commit()
        cursor.execute("SELECT * FROM GAMES WHERE g_name = %s", (data['name'],))
        result = cursor.fetchone()
        if result:
            id, name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stock_count, open_ = result
            new_game = GameBrain(Game(id, name, total_turns, sec_per_turn, starting_money, turns_between_events,
                                      player_count, stock_count, open_),
                                 new_turn_callback=lambda: handle_next_turn(id))
            gameBrains[1] = new_game
            print(id)
        else:
            return None
        return jsonify({'message': 'Game Created', 'game_id': id}), 201
    except Exception as e:
        return {'message': str(e)}
    finally:
        cursor.close()
        connection.close()


@game_blueprint.route('/games', methods=['GET'])
def get_all():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM GAMES")
        results = cursor.fetchall()
        print(gameBrains[1])
        return jsonify({'games': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@game_blueprint.route('/game/id/<int:game_id>', methods=['GET'])
def get_by_id(game_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM GAMES WHERE g_id = %s", (game_id,))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'error': 'game not found'}), 404
        return jsonify({'game': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@game_blueprint.route('/game/name/<string:game_name>', methods=['GET'])
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
