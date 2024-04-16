from flask import Blueprint, request, jsonify, make_response
import json
from src import db

communities = Blueprint('communities', __name__)

@communities.route('/exchange-focused', methods=['GET'])
def find_exchange_communities():
    cur = db.get_db().cursor()
    cur.execute("""
        SELECT CommunityID, Name, Description
        FROM Community
        WHERE Description LIKE '%textbook exchange%';
    """)
    communities = cur.fetchall()
    return jsonify(communities)

@communities.route('/', methods=['POST'])
def create_community():
    community_data = request.json
    cur = db.get_db().cursor()
    cur.execute("""
        INSERT INTO Community (Name, Description) 
        VALUES (%s, %s);
    """, (community_data['Name'], community_data['Description']))
    db.commit()
    return jsonify({"success": True}), 201



