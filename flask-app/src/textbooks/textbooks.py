from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

textbooks = Blueprint('textbooks', __name__)

@textbooks.route('/textbooks', methods=['GET'])
def get_textbooks():
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT textbooks.TextbookID, textbooks.Title, textbooks.Author, textbooks.ISBN, ExchangeOffer.Price 
    FROM textbooks 
    JOIN ExchangeOffer ON textbooks.TextbookID = ExchangeOffer.TextbookID 
    ORDER BY ExchangeOffer.Price ASC
    ''')
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


# User Story 1
@textbooks.route('/affordable_textbooks/<int:max_price>', methods=['GET'])
def get_affordable_textbooks(max_price):
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT textbooks.TextbookID, Title, Author, ISBN, Price
    FROM textbooks
    JOIN ExchangeOffer ON textbooks.TextbookID = ExchangeOffer.TextbookID
    WHERE Price <= %s
    ORDER BY Price ASC
    ''', (max_price,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)




# User Story 2
@textbooks.route('/textbooks/user_textbooks/<int:user_id>', methods=['GET'])
def get_user_textbooks(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT TextbookID, Title, Author, ISBN
    FROM textbooks
    WHERE TextbookID IN (
        SELECT TextbookID
        FROM ExchangeOffer
        WHERE UserID = %s
    )
    ''', (user_id,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)



