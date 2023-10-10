from flask import Blueprint, jsonify, request
from ..snowflake_connection import connect_snowflake

# Blueprint
player_to_game_blueprint = Blueprint('player_to_game', __name__)


@player_to_game_blueprint.route('/player_to_game_relation', methods=['POST'])
def create():
    data = request.get_json()
    required_fields = ['game_id', 'player_id', 'turn_id', 'amount_of_money']

    if not all(field in data for field in required_fields):
        return {'message': 'Required game data is missing'}

    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO PLAYERS_TO_GAME (ptg_player_id,ptg_game_id, ptg_turn_id, ptg_money_amount) VALUES (%s, %s, %s, %s)",
            (data['player_id'], data['game_id'], data['turn_id'], data['amount_of_money'])
        )
        connection.commit()
        return {'message': 'Player_To_Game created successfully'}
    except Exception as e:
        return {"message": str(e)}
    finally:
        cursor.close()
        connection.close()


@player_to_game_blueprint.route('/player_to_game_relation/<int:game_id>&<int:player_id>&<int:turn_id>', methods=['GET'])
def get_by_id(game_id, player_id, turn_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM PLAYERS_TO_GAME WHERE ptg_game_id = %s AND ptg_player_id = %s AND ptg_turn_id = %s",
            (game_id, player_id, turn_id)
        )
        relation = cursor.fetchone()
        if relation is None:
            return jsonify({'error': 'Relation not found'}), 404

        return jsonify({'relation': relation}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@player_to_game_blueprint.route('/player_to_game_relation/<int:game_id>&<int:turn_id>', methods=['GET'])
def get_all_by_player_in_game(cls, game_id, turn_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM PLAYERS_TO_GAME WHERE ptg_game_id = %s AND ptg_turn_id = %s",
            (game_id, turn_id)
        )
        relations = cursor.fetchall()
        if relations is None:
            return jsonify({'error': 'Relations not found'}), 404

        return jsonify({'relation': relations}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
