from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

online_resources = Blueprint('online_resources', __name__)