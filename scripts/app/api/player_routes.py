from flask import jsonify, request
from . import api_blueprint
from ...snowflake_connection import connect_snowflake

@api_blueprint.route('/players', methods=['GET'])
def get_players():
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


@api_blueprint.route('/player/<int:player_id>', methods=['GET'])
def get_player(player_id):
    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM PLAYERS WHERE PLAYER_ID = %s", (player_id,))
        player = cursor.fetchone()

        if player is None:
            return jsonify({'error': 'Player not found'}), 404

        return jsonify({'player': player}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@api_blueprint.route('/player', methods=['POST'])
def create_player():
    data = request.get_json()

    # Basic input validation
    required_fields = ['player_name', 'player_email']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required player data is missing'}), 400

    player_name = data['player_name']
    player_email = data['player_email']

    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO PLAYERS (PLAYER_NAME, PLAYER_EMAIL) VALUES (%s, %s)",
            (player_name, player_email)
        )
        connection.commit()

        return jsonify({'message': 'Player created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

