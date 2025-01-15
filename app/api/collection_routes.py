# from datetime import dateime, timezone
# from flask import Blueprint, jsonify, current_app, request, json
# from flask_login import login_required, current_user
# from sqlalchemy.exc import SQLAlchemyError
# from app.models import db, Collection, Recipe


# collection_routes = Blueprint('collections', __name__)


# @collection_routes.route('/', methods=["GET"])
# def collections():
#     """Query to get all collections and return them in a list of collection dictionaries"""

#     try:
#         # Fetch all collections
#         collections = Collection.query.all()

#         # If no collection is found, return an empty list with a success message

#         if not collections:
#             return jsonify({
#                 'message': 'No collections found',
#                 'collections': []
#             }), 200

#         # Make an empty list to store all collections
#         all_collections_list = []

#         # Go through each collection
#         for collection in collections:
