from flask import Blueprint, jsonify, request
from ..snowflake_connection import connect_snowflake

player_blueprint = Blueprint('player', __name__)


@player_blueprint.route('/player', methods=['POST'])
def create():
    data = request.get_json()
    required_fields = ['name']

    if not all(field in data for field in required_fields):
        return {'message': 'Required player data is missing'}

    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        result = cursor.execute("""
            INSERT INTO PLAYERS (
                pl_name
            ) VALUES (%s)
        """, (data['name']))
        connection.commit()
        print(result)
        return jsonify({'message': 'Player created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@player_blueprint.route('/players', methods=['GET'])
def get_all():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM PLAYERS")
        players = cursor.fetchall()
        return jsonify({'players': players}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@player_blueprint.route('/players/open', methods=['GET'])
def get_all_players_in_open_games():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT PL_ID,PL_NAME,G_ID FROM PLAYERS JOIN PLAYERS_TO_GAME ON pl_id = ptg_player_id "
            "JOIN GAMES ON g_id = ptg_game_id WHERE g_is_open = TRUE",
        )
        relations = cursor.fetchall()
        if relations is None:
            return jsonify({'error': 'Players not found'}), 404

        return jsonify({'players': relations}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@player_blueprint.route('/player/<int:player_id>', methods=['GET'])
def get_by_id(player_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM PLAYERS WHERE pl_id = %s", (player_id,))
        player = cursor.fetchone()

        if player is None:
            return jsonify({'error': 'Player not found'}), 404

        return jsonify({'player': player}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
