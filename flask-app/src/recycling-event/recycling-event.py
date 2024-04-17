from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

recycling_event = Blueprint('recycling_event', __name__)

# Get all recycling events from the DB
@recycling_event.route('/recycling_event', methods=['GET'])
def get_recycling_events():
    cursor = db.get_db().cursor()
    cursor.execute('select eventID, location, date, description')

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# gets the recycling events associated with the given user
@recycling_event.route('/recycling_event/<int:user_id>', methods=['GET'])
def get_user_recycling_event(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
    SELECT RecyclingEvent.eventID, RecyclingEvent.location, RecyclingEvent.date, RecyclingEvent.description
    FROM RecyclingEvent
    JOIN EventParticipation ON EventParticipation.EventID = RecyclingEvent.EventID
    WHERE UserID = %s
    ''', (user_id,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# creates a event participation for the given user
@recycling_event.route('/recycling_event/<int:user_id>', methods=['POST'])
def add_event_participation(user_id):

    # Collecting data from the request JSON
    data = request.get_json()
    current_app.logger.info(data)

    # Extracting variables from the data
    eventID = data['EventID']
    role = data['Role']

    # Constructing the SQL query
    query = '''
    INSERT INTO EventParticipation (UserID, EventID, role)
    VALUES (%s, %s, %s);
    '''

    # Executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query, (user_id, eventID, role))
    db.get_db().commit()

    return jsonify({'success': 'Event participation posted successfully'}), 201


# updates event participation given a user id and new participation
@recycling_event.route('/update_participation', methods=['PUT'])
def update_event_participation():
    print("Received data:", request.json)  # Debug line to check what's received
    participation_info = request.json
    if 'user_id' not in participation_info or 'new_participation' not in participation_info:
        return jsonify({'error': 'Both user_id and new_participation are required'}), 400

    user_id = participation_info['user_id']
    new_participation = participation_info['new_participation']

    query = '''
    UPDATE EventParticipation
    SET Role = %s
    WHERE UserID = %s;
    '''
    cursor = db.get_db().cursor()
    r = cursor.execute(query, (new_participation, user_id))
    db.get_db().commit()
    
    if r:
        return jsonify({'success': 'Participation updated successfully'}), 200
    else:
        return jsonify({'error': 'No records updated, check your user_id'}), 404

# unsubscribes this user from all events
@recycling_event.route('/remove_participation/<int:user_id>', methods=['DELETE'])
def remove_user_from_all_events(user_id):
    query = '''
    DELETE FROM EventParticipation
    WHERE UserID = %s;
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (user_id,))
    db.get_db().commit()
    
    return jsonify({'success': 'User removed successfully'}), 200

# unsubscribes this user from the given event
@recycling_event.route('/remove_event_participation/<int:user_id>/<int:event_id>', methods=['DELETE'])
def unsubscribe_from_event(user_id, event_id):

    query = '''
    DELETE FROM EventParticipation
    WHERE EventID = %s AND UserID = %s;
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (event_id, user_id))
    db.get_db().commit()
    
    return jsonify({'success': 'Participation removed successfully'}), 200
