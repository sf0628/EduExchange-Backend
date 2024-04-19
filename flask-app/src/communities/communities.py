from flask import Blueprint, request, jsonify, make_response
import json
from src import db

communities = Blueprint('communities', __name__)

# get all community information 
@communities.route('/exchange-focused', methods=['GET'])
def find_exchange_communities():
    cursor = db.get_db().cursor()
    cursor.execute("""
        SELECT CommunityID, Name, Description
        FROM Community;
    """)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# get all sharing session information for a community
@communities.route('/get_sharing_sessions/<int:community_id>', methods=['GET'])
def get_sharing_sessions(community_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT SharingSession.SessionID, SharingSession.Schedule, SharingSession.CommunityID, SharingSession.ResourceID
    FROM SharingSession
    JOIN Community ON Community.CommunityID = SharingSession.CommunityID
    WHERE Community.CommunityID = %s
    ''', (community_id,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# get all sharing session information
@communities.route('/get_all_sharing_sessions', methods=['GET'])
def get_all_sharing_sessions():
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT *
    FROM SharingSession
    ''')
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# get all sharing session information
@communities.route('/get_all_resources', methods=['GET'])
def get_all_resources():
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT *
    FROM DigitalResource
    ''')
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# get information of particular sharing session
@communities.route('/sharing_info/<int:community_id>', methods=['GET'])
def get_sharing_info(community_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT SharingSession.SessionID, SharingSession.Schedule, SharingSession.CommunityID, SharingSession.ResourceID
    FROM SharingSession
    WHERE CommunityID = %s
    ''', (community_id,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# creates sharing sessions
@communities.route('/sharing_sessions', methods=['POST'])
def create_sharing_session():
    # Extract data from the request
    data = request.get_json()  # Ensures that data is properly extracted as JSON
    community_name = data.get('community')
    resource_title = data.get('resource')
    schedule = data.get('schedule')

    cursor = db.get_db().cursor()

    # Retrieve CommunityID
    cursor.execute("SELECT CommunityID FROM Community WHERE Name = %s", (community_name,))
    community_result = cursor.fetchone()
    if not community_result:
        return jsonify({"error": "Community not found"}), 404
    community_id = community_result[0]

    # Retrieve ResourceID
    cursor.execute("SELECT ResourceID FROM DigitalResource WHERE Title = %s", (resource_title,))
    resource_result = cursor.fetchone()
    if not resource_result:
        return jsonify({"error": "Resource not found"}), 404
    resource_id = resource_result[0]

    # Check if schedule is provided
    if not schedule:
        return jsonify({"error": "Schedule is required"}), 400

    # Insert the new sharing session into the database
    try:
        cursor.execute(
            "INSERT INTO SharingSession (CommunityID, Schedule, ResourceID) VALUES (%s, %s, %s)",
            (community_id, schedule, resource_id)
        )
        db.get_db().commit()
        return jsonify({"success": "Sharing session created successfully"}), 201
    except Exception as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500
    
# deletes a sharing session
@communities.route('/delete_sharing_session/<int:session_id>', methods=['DELETE'])
def delete_sharing_session(session_id):
    # Check if the session exists
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM SharingSession WHERE SessionID = %s', (session_id,))
    session = cursor.fetchone()
    if session is None:
        return jsonify({"error": "Session not found"}), 404

    try:
        cursor.execute('DELETE FROM SharingSession WHERE SessionID = %s', (session_id,))
        db.get_db().commit()
        return jsonify({"success": "Session deleted successfully"}), 200
    except Exception as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500
    
# get all membership information for a user
@communities.route('/user_member/<int:user_id>', methods=['GET'])
def get_user_member(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT Community.Name as CommunityName, Membership.Role, User.Name as UserName
    FROM Membership
    JOIN Community ON Membership.CommunityID = Community.CommunityID
    JOIN User ON User.UserID = Membership.UserID
    WHERE Membership.UserID = %s
    ''', (user_id,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# get all membership information for a community
@communities.route('/community_member/<int:community_id>', methods=['GET'])
def get_community_member(community_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT membership.SessionID, membership.UserID, membership.CommunityID
    FROM membership
    JOIN Community ON Community.CommunityID = membership.CommunityID
    WHERE CommunityID = %s
    ''', (community_id,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# Removes a member from the community
@communities.route('/remove-member', methods=['DELETE'])
def remove_member():
    member_data = request.json
    # Check if all required fields are provided
    if 'community_id' not in member_data or 'user_id' not in member_data:
        return jsonify({'error': 'community_id and user_id are required fields'}), 400
    community_id = member_data['community_id']
    user_id = member_data['user_id']
    # Check if the provided community and user exist
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Community WHERE CommunityID = %s', (community_id,))
    community = cursor.fetchone()
    cursor.execute('SELECT * FROM User WHERE UserID = %s', (user_id,))
    user = cursor.fetchone()
    
    if community is None:
        return jsonify({'error': 'Community does not exist'}), 404
    
    if user is None:
        return jsonify({'error': 'User does not exist'}), 404
    
    # Check if the user is a member of the community
    cursor.execute('SELECT * FROM Membership WHERE CommunityID = %s AND UserID = %s', (community_id, user_id))
    membership = cursor.fetchone()
    
    if membership is None:
        return jsonify({'error': 'User is not a member of the community'}), 404
    
    # Remove the user from the Membership table
    try:
        cursor.execute('DELETE FROM Membership WHERE CommunityID = %s AND UserID = %s', (community_id, user_id))
        db.get_db().commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# insert new community
@communities.route('/create_community', methods=['POST'])
def create_community():
    try:
        # Get JSON data from the request
        community_data = request.json
        
        # Validate required fields
        if 'Name' not in community_data or 'Description' not in community_data:
            return jsonify({"error": "Name and Description are required"}), 400
        
        # Insert new community into the database
        with db.get_db().cursor() as cur:
            cur.execute("""
                INSERT INTO Community (Name, Description) 
                VALUES (%s, %s);
            """, (community_data['Name'], community_data['Description']))
        
        # Commit the transaction
        db.get_db().commit()
        
        # Return success response
        return jsonify({"success": True}), 201
    except Exception as e:
        # Handle exceptions and return appropriate error response
        return jsonify({"error": str(e)}), 500

# update community description
@communities.route('/update_description', methods=['PUT'])
def update_community():
    print("Received data:", request.json)  # Debug line to check what's received
    condition_info = request.json
    if 'community_id' not in condition_info or 'new_description' not in condition_info:
        return jsonify({'error': 'Both community_id and new_description are required'}), 400

    community_id = condition_info['community_id']
    new_description = condition_info['new_description']

    query = '''
    UPDATE Community
    SET Description = %s
    WHERE CommunityID = %s;
    '''
    cursor = db.get_db().cursor()
    r = cursor.execute(query, (new_description, community_id))
    db.get_db().commit()
    if r:
        return jsonify({'success': 'Description updated successfully'}), 200
    else:
        return jsonify({'error': 'No records updated, check your offer_id'}), 404
    
# adds new member
@communities.route('/add-member', methods=['POST'])
def add_member():
    member_data = request.json
    # Check if all required fields are provided
    if 'community_id' not in member_data or 'user_id' not in member_data or 'role' not in member_data:
        return jsonify({'error': 'community_id, user_id, and role are required fields'}), 400
    community_id = member_data['community_id']
    user_id = member_data['user_id']
    role = member_data['role']
    # Check if the provided community and user exist
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Community WHERE CommunityID = %s', (community_id,))
    community = cursor.fetchone()
    cursor.execute('SELECT * FROM User WHERE UserID = %s', (user_id,))
    user = cursor.fetchone()
    
    if community is None:
        return jsonify({'error': 'Community does not exist'}), 404
    
    if user is None:
        return jsonify({'error': 'User does not exist'}), 404
    
    # Add the user to the Membership table
    try:
        cursor.execute("""
        INSERT INTO Membership (CommunityID, UserID, Role) 
         VALUES (%s, %s, %s);
        """, (community_id, user_id, role))
        db.get_db().commit()
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
