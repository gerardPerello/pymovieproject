from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

from . import (player_routes,
               game_routes,
               transaction_routes,
               currency_routes,
               event_routes,
               event_to_stock_routes,
               forex_to_stocks_routes,
               forex_history_routes,
               stock_market_routes,
               stock_routes,
               player_to_game_routes,
               portfolio_routes)
from .extraTransactions import future_transaction_routes, instant_transaction_routes
