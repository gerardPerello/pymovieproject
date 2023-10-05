from flask import Blueprint, jsonify, request
from ...snowflake_connection import connect_snowflake

player_to_game_blueprint = Blueprint('player_to_game', __name__)


# GET all player-to-game relations
@player_to_game_blueprint.route('/player_to_game_relations', methods=['GET'])
def get_player_to_game_relations():
    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM PLAYERS_IN_GAME")
        relations = cursor.fetchall()
        return jsonify({'relations': relations}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# GET a single player-to-game relation
@player_to_game_blueprint.route('/player_to_game_relation/<int:relation_id>', methods=['GET'])
def get_player_to_game_relation(relation_id):
    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM PLAYERS_IN_GAME WHERE RELATION_ID = %s", (relation_id,))
        relation = cursor.fetchone()

        if relation is None:
            return jsonify({'error': 'Relation not found'}), 404

        return jsonify({'relation': relation}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# POST a new player-to-game relation
@player_to_game_blueprint.route('/player_to_game_relation', methods=['POST'])
def create_player_to_game_relation():
    data = request.get_json()
    required_fields = ['player_id', 'game_id', 'turn_id']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required data is missing'}), 400

    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO PLAYERS_IN_GAME (PLAYER_ID, GAME_ID, TURN_ID) 
            VALUES (%s, %s)
            """,
            (data['player_id'], data['game_id'], data['turn_id'])
        )
        connection.commit()
        return jsonify({'message': 'Relation created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
