from flask  import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Client, Membership
from app import db
from datetime import datetime, timedelta

bp = Blueprint('membership', __name__)

@bp.route('/current-plan', methods=['GET'])
@jwt_required()
def current_plan():
    current_user = User.query.get(get_jwt_identity())
    client = Client.query.filter_by(user_id=current_user.id).first()
    membership = Membership.query.filter_by(client_id=client.id).order_by(Membership.end_date.desc()).first()
    
    if not membership:
        return jsonify({"msg": "No active membership found"}), 404
    
    return jsonify({
        "plan_type": membership.plan_type,
        "start_date": membership.start_date.strftime('%Y-%m-%d'),
        "end_date": membership.end_date.strftime('%Y-%m-%d')
    }), 200

@bp.route('/switch-plan', methods=['POST'])
@jwt_required()
def switch_plan():
    current_user = User.query.get(get_jwt_identity())
    client = Client.query.filter_by(user_id=current_user.id).first()
    data = request.get_json()
    
    new_plan_type = data['plan_type']
    start_date = datetime.now().date()
    
    if new_plan_type == 'monthly':
        end_date = start_date + timedelta(days=30)
    elif new_plan_type == 'yearly':
        end_date = start_date + timedelta(days=365)
    else:
        return jsonify({"msg": "Invalid plan type"}), 400
    
    new_membership = Membership(
        client_id=client.id,
        plan_type=new_plan_type,
        start_date=start_date,
        end_date=end_date
    )
    db.session.add(new_membership)
    db.session.commit()
    
    return jsonify({"msg": "Membership plan switched successfully"}), 200

@bp.route('/available-plans', methods=['GET'])
def available_plans():
    plans = [
        {
            "name": "Monthly",
            "price": "$49.99",
            "features": ["Access to gym", "Group classes", "Personal trainer (2 sessions)"]
        },
        {
            "name": "Yearly",
            "price": "$499.99",
            "features": ["Access to gym", "Unlimited group classes", "Personal trainer (24 sessions)", "Nutrition consultation"]
        }
    ]
    return jsonify(plans), 200