from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Client, Membership
from app import db

bp = Blueprint('admin', __name__)

@bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'admin':
        return jsonify({"msg": "Access denied"}), 403
    
    total_users = User.query.count()
    total_clients = Client.query.count()
    active_memberships = Membership.query.filter(Membership.end_date >= db.func.current_date()).count()
    
    return jsonify({
        "total_users": total_users,
        "total_clients": total_clients,
        "active_memberships": active_memberships
    }), 200

@bp.route('/recent-activity', methods=['GET'])
@jwt_required()
def recent_activity():
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'admin':
        return jsonify({"msg": "Access denied"}), 403
    
    # This is a placeholder. In a real app, you'd implement logic to fetch recent activities.
    activities = [
        {"user": "John Doe", "action": "Logged in", "date": "2023-05-01 09:00"},
        {"user": "Jane Smith", "action": "Updated profile", "date": "2023-05-01 10:30"},
        {"user": "Mike Johnson", "action": "Completed workout", "date": "2023-05-01 11:45"}
    ]
    
    return jsonify(activities), 200