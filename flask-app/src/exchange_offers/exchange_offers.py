from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

exchange_offers = Blueprint('exchange_offers', __name__)


@exchange_offers.route('/all_exchange_books', methods=['GET'])
def get_all_exchange_books():
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT textbooks.TextbookID, textbooks.Title, textbooks.Author, textbooks.ISBN, ExchangeOffer.Price, ExchangeOffer.ConditionState
    FROM textbooks
    JOIN ExchangeOffer ON ExchangeOffer.TextbookID = textbooks.TextbookID
    ORDER BY textbooks.Title
    ''')
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


@exchange_offers.route('/user_textbooks/<int:user_id>', methods=['GET'])
def get_user_textbooks(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT textbooks.TextbookID, textbooks.Title, textbooks.Author, textbooks.ISBN
    FROM textbooks
    JOIN ExchangeOffer ON ExchangeOffer.TextbookID = textbooks.TextbookID
    WHERE UserID = %s
    ''', (user_id,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


@exchange_offers.route('/post_exchange/<userID>', methods=['POST'])
def post_exchange2(userID):
    # Collecting data from the request JSON
    data = request.get_json()
    current_app.logger.info(data)

    # Extracting variables from the data
    title = data['Title']
    author = data['Author']
    isbn = data['ISBN']
    # user_id = data['UserID']
    condition = data['ConditionState']
    price = data['Price']

    # Constructing the SQL query
    query = '''
    INSERT INTO ExchangeOffer (TextbookID, UserID, ConditionState, Price)
    VALUES ((SELECT TextbookID FROM textbooks WHERE Title=%s AND Author=%s AND ISBN=%s), %s, %s, %s)
    '''
    current_app.logger.info(query)

    # Executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query, (title, author, isbn, userID, condition, price))
    db.get_db().commit()

    return jsonify({'success': 'Exchange offer posted successfully'})

@exchange_offers.route('/donate_material', methods=['PUT'])
def donate_material():
    try:
        user_id = request.json.get('user_id')
        textbook_id = request.json.get('textbook_id')

        query = '''
        UPDATE ExchangeOffer 
        SET Price = 0 
        WHERE UserID = %s AND TextbookID = %s;
        '''
        cursor = db.get_db().cursor()
        cursor.execute(query, (user_id, textbook_id))
        db.get_db().commit()
        
        return jsonify({'success': 'Material donated successfully'}), 200
    except MySQLError as e:
        # Log the error for debugging
        print(f"Database Error: {e}")
        return jsonify({'error': 'Failed to update the material'}), 500
    except Exception as e:
        # Log the error for debugging
        print(f"General Error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

