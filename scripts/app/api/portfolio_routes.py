from flask import Blueprint, jsonify, request
from ...snowflake_connection import connect_snowflake

portfolio_blueprint = Blueprint('portfolio', __name__)


# GET all portfolios
@portfolio_blueprint.route('/portfolios', methods=['GET'])
def get_portfolios():
    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM PORTFOLIOS")
        portfolios = cursor.fetchall()
        return jsonify({'portfolios': portfolios}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# GET a single portfolio
@portfolio_blueprint.route('/portfolio/<int:portfolio_id>', methods=['GET'])
def get_portfolio(portfolio_id):
    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM PORTFOLIOS WHERE PORTFOLIO_ID = %s", (portfolio_id,))
        portfolio = cursor.fetchone()

        if portfolio is None:
            return jsonify({'error': 'Portfolio not found'}), 404

        return jsonify({'portfolio': portfolio}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# POST a new portfolio
@portfolio_blueprint.route('/portfolio', methods=['POST'])
def create_portfolio():
    data = request.get_json()
    required_fields = ['player_id','game_id','turn_id', 'currency_id', 'amount']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Required data is missing'}), 400

    connection = connect_snowflake()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO PORTFOLIOS (PLAYER_ID, GAME_ID, TURN_ID, CURRENCY_ID, AMOUNT) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (data['player_id'],data['game_id'],data['turn_id'], data['currency_id'], data['amount'])
        )
        connection.commit()
        return jsonify({'message': 'Portfolio created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
