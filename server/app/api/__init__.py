# This can be an empty file or can be used to export your classes for easier importing elsewhere in your app.
from . import (currency_routes, game_routes, player_to_game_routes, player_routes)
from flask import Blueprint

api_blueprint = Blueprint('models', __name__)

api_blueprint.register_blueprint(game_routes.game_blueprint, url_prefix='/game')
api_blueprint.register_blueprint(currency_routes.currency_blueprint, url_prefix='/currency')
api_blueprint.register_blueprint(player_routes.player_blueprint, url_prefix='/player')
api_blueprint.register_blueprint(player_to_game_routes.player_to_game_blueprint, url_prefix='/playertogame')
