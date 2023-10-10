from flask_socketio import emit,join_room, leave_room
from .. import socketio
from ..logic import *
from ..models import Game

@socketio.on('connect')
def handle_connect():
    print("Client Connected")
    # This might be replaced by a message sent from the client upon connecting,
    # which provides the player_id and game_id.

@socketio.on('disconnect')
def handle_disconnect():
    print("Client Disconnected")
    # You would probably remove the player from the gameBrain instance here,
    # assuming you have a mechanism for identifying which player disconnected.

@socketio.on('join_game')
def handle_join_game(data):
    player_id = data.get('player_id')
    game_id = data.get('game_id')

    # Join the player to a room specific to the game.
    join_room(game_id)
    if game_id not in gameBrains:
        print("Creating new game!!")
        game = Game.get_by_id(game_id)
        create_game(game_id, game, handle_next_turn(game_id))
    game_logic = gameBrains.get(game_id)
    print(game_logic)
    if game_logic:
        game_logic.add_connected_player(player_id)



@socketio.on('leave_game')
def handle_leave_game(data):
    player_id = data.get('player_id')
    game_id = data.get('game_id')

    # Remove the player from a room specific to the game.
    leave_room(game_id)

    game_logic = gameBrains.get(game_id)
    if game_logic:
        game_logic.remove_connected_player(player_id)

    emit('player_left', {'player_id': player_id}, room=game_id)


# Server-side Python
@socketio.on('player_ready')
def handle_player_ready(data):
    game_id = data.get('game_id')
    player_id = data.get('player_id')
    # You might retrieve the relevant GameLogic instance from a dictionary using game_id
    game_logic = gameBrains[game_id]
    game_logic.set_player_ready(player_id)
    print(data)

    if game_logic.all_players_ready_to_change_turn():
        handle_next_turn(game_id)


def handle_next_turn(game_id):
    #game_logic = gameBrains[game_id]
    #game_logic.end_of_turn_logic()

    # Notify clients of new turn state
    emit('new_turn', room=game_id)
