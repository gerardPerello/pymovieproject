# __init__.py

from .game_logic import GameBrain

# You might manage games by ID or some other identifier.
gameBrains = {}

def create_game(gameBrain_id, game, callback):
    # Initialize a new game with its initial state and store it in games dict.
    gameBrains[gameBrain_id] = GameBrain(game, callback)

def get_gameBrain(gameBrain_id):
    # Retrieve the game instance by its ID.
    return gameBrains.get(gameBrain_id)

def delete_gameBrain(gameBrain_id):
    # Clean up the game instance when it's no longer needed.
    if gameBrain_id in gameBrains:  # Corrected this line
        del gameBrains[gameBrain_id]

def change_state(gameBrain_id, new_state):
    # Update the state of the game.
    gameBrain = get_gameBrain(gameBrain_id)
    if gameBrain:
        gameBrain.set_state(new_state)
        gameBrain.execute()
