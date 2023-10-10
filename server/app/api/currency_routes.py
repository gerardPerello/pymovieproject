from flask import Blueprint, jsonify, request
from ..snowflake_connection import connect_snowflake
# Blueprint
currency_blueprint = Blueprint('currency', __name__)


# GET all currencies
@currency_blueprint.route('/currencies', methods=['GET'])
def get_all():
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM CURRENCIES")
        results = cursor.fetchall()
        return jsonify({'currencies': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@currency_blueprint.route('/values/<int:game_id>/<int:turn_id>', methods=['GET'])
def get_all_players_in_open_games(game_id, turn_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "select s_id, s_name, sm_turn_id, sm_game_id, sm_stock_value from stock_market "
            "join stocks on sm_stock_id = s_id "
            "where sm_turn_id = %s and sm_game_id = %s",(turn_id, game_id,)
        )
        relations = cursor.fetchall()
        if relations is None:
            return jsonify({'error': 'Values for Stocks not found'}), 404

        return jsonify({'values': relations}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()



# GET a single currency by ID
@currency_blueprint.route('/currency/<int:currency_id>', methods=['GET'])
def get_by_id(currency_id):
    connection = connect_snowflake()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM CURRENCIES WHERE C_ID = %s", (currency_id,))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'error': 'Currency not found'}), 404
        return jsonify({'currency': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
