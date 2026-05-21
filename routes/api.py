from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/v1', methods=['GET'])
def api_root():
    return jsonify({
        'message': 'MindBreath AI API v1',
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'API root'},
            {'path': '/health', 'method': 'GET', 'description': 'Health check'},
        ]
    })

# Add your API routes here
# Example:
# @api_bp.route('/api/v1/users', methods=['GET'])
# def get_users():
#     from models.database import db
#     from models.user import User
#     users = User.query.all()
#     return jsonify([user.to_dict() for user in users])
