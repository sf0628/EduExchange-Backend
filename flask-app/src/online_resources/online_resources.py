from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

online_resources = Blueprint('online_resources', __name__)

# User Story 1 -- textbooks
@online_resources.route('/affordable_textbooks/<int:max_price>', methods=['GET'])
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


# User Story 2 -- textbooks
@online_resources.route('/user_textbooks/<int:user_id>', methods=['GET'])
def get_user_textbooks(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT TextbookID, Title, Author, ISBN
    FROM textbooks
    WHERE UserID = %s
    ''', (user_id,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# User Story 4 -- textbooks
@online_resources.route('/add_textbook/<int:user_id>', methods=['POST'])
def add_textbook(user_id):
    # Collecting data from the request JSON
    data = request.get_json()
    isbn = data.get('isbn')
    author = data.get('author')
    title = data.get('title')

    # Constructing the SQL query
    query = '''
    INSERT INTO textbooks (ISBN, Author, Title, UserID) 
    VALUES (%s, %s, %s, %s);
    '''
    
    # Executing the SQL query
    cursor = db.get_db().cursor()
    cursor.execute(query, (isbn, author, title, user_id))
    db.get_db().commit()
    
    return jsonify({'success': 'Textbook added successfully'}), 201

# User Story 5 -- textbooks
@online_resources.route('/delete_textbook/<int:user_id>/<int:textbook_id>', methods=['DELETE'])
def delete_textbook(user_id, textbook_id):
    cursor = db.get_db().cursor()
    # First, verify the textbook belongs to the user
    cursor.execute('SELECT * FROM textbooks WHERE TextbookID = %s AND UserID = %s', (textbook_id, user_id))
    result = cursor.fetchone()
    if not result:
        return jsonify({'error': 'Textbook not found or not owned by user'}), 404

    # Proceed to delete the textbook if verification passes
    cursor.execute('DELETE FROM textbooks WHERE TextbookID = %s AND UserID = %s', (textbook_id, user_id))
    db.get_db().commit()
    return jsonify({'success': 'Textbook deleted successfully'}), 200


# view all the digital resources available on the platform
@online_resources.route('/view-resources', methods=['GET'])
def view_all():
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT ResourceID, Title, Format, AccessUrl
    FROM DigitalResource
    ''')
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)


# view the details of a specific digital resource
@online_resources.route('/view-resources/<int:resource_id>', methods=['GET'])
def view_this(resource_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT Title, Format, AccessUrl
    FROM DigitalResource
    WHERE ResourceID = %s
    ''', (resource_id,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

#creates an empty wishlist of items that the user can add to
@online_resources.route('/create-wishlist', ['POST'])
def create_wishlist(user_id):
    # Collecting data from the request JSON
    data = request.get_json()
    name = data.get('Name')

    # Constructing the SQL query
    query = '''
    INSERT INTO Wishlist (Name, UserID) 
    VALUES (%s, %s);
    '''
    # Executing the SQL query
    cursor = db.get_db().cursor()
    cursor.execute(query, (name, user_id))
    db.get_db().commit()
    
    return jsonify({'success': 'Wishlist created successfully'}), 201

# deletes a wishlist
@online_resources.route('/delete_wishlist/<int:user_id>/<int:wishlist_id>', methods=['DELETE'])
def delete_wishlist(user_id, wishlist_id):
    cursor = db.get_db().cursor()
    # First, verify the wishlist belongs to the user
    cursor.execute('SELECT * FROM Wishlist WHERE WishlistID = %s AND UserID = %s', (wishlist_id, user_id))
    result = cursor.fetchone()
    if not result:
        return jsonify({'error': 'Wishlist not found or not owned by user'}), 404

    # Proceed to delete the wishlist if verification passes
    cursor.execute('DELETE FROM Wishlist WHERE WishlistID = %s AND UserID = %s', (wishlist_id, user_id))
    db.get_db().commit()
    return jsonify({'success': 'Wishlist deleted successfully'}), 200


# adds an item to the given wishlist
@online_resources.route('/add-textbook-to-wishlist', ['POST'])
def add_textbook_to_wishlist(wishlist_id, textbook_id):
    cursor = db.get_db().cursor()
    query = "INSERT INTO WishlistItem (WishlistID, TextbookID) VALUES (%s, %s);"
    try:
        cursor.execute(query, (wishlist_id, textbook_id))
        db.get_db().commit() 
        return True
    except Exception as e:
        print("An error occurred:", e)
        db.get_db().rollback()  # Rollback in case of error
        return False

# removes the given item from the given wishlist, provided it exists
@online_resources.route('/remove-textbook-from-wishlist', ['DELETE'])
def remove_textbook_from_wishlist(wishlist_id, textbook_id):
    # Assuming `db` is your database connection object
    cursor = db.get_db().cursor()
    query = "DELETE FROM WishlistItem WHERE WishlistID = %s AND TextbookID = %s;"
    try:
        cursor.execute(query, (wishlist_id, textbook_id))
        db.get_db().commit() 
        return True
    except Exception as e:
        print("An error occurred:", e)
        db.get_db().rollback()  # Rollback in case of error
        return False

