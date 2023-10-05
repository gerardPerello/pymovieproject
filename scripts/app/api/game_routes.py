from flask import jsonify, request
from . import api_blueprint
from ...snowflake_connection import connect_snowflake

@api_blueprint.route('/games', methods=['GET'])
def get_games():
    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM GAMES")
        games = cursor.fetchall()

        return jsonify({'games': games}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@api_blueprint.route('/game/<int:game_id>', methods=['GET'])
def get_game(game_id):
    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM GAMES WHERE GAME_ID = %s", (game_id,))
        game = cursor.fetchone()

        if game is None:
            return jsonify({'error': 'Game not found'}), 404

        return jsonify({'game': game}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@api_blueprint.route('/game', methods=['POST'])
def create_game():
    data = request.get_json()

    # Basic input validation
    required_fields = ['game_name', 'total_turns', 'sec_per_turn', 'starting_money', 'turns_between_events',
                       'player_count', 'stocks_count']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required game data is missing'}), 400

    game_name = data['game_name']
    total_turns = data['total_turns']
    sec_per_turn = data['sec_per_turn']
    starting_money = data['starting_money']
    turns_between_events = data['turns_between_events']
    player_count = data['player_count']
    stocks_count = data['stocks_count']

    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO GAMES (NAME, TOTAL_TURNS, SECONDS_PER_TURN, STARTING_MONEY, TURNS_BETWEEN_EVENTS, "
            "PLAYER_COUNT, STOCKS_COUNT) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (game_name, total_turns, sec_per_turn, starting_money, turns_between_events, player_count, stocks_count)
        )
        connection.commit()

        return jsonify({'message': 'Game created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# ... Additional routes for updating, deleting games