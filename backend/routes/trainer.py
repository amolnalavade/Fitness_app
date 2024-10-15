from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Client, DietPlan
from app import db

bp = Blueprint('trainer', __name__)

@bp.route('/clients', methods=['GET'])
@jwt_required()
def get_clients():
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'trainer':
        return jsonify({"msg": "Access denied"}), 403
    
    clients = Client.query.all()
    return jsonify([{
        "id": client.id,
        "name": client.name,
        "age": client.age,
        "height": client.height,
        "weight": client.weight,
        "goals": client.goals
    } for client in clients]), 200

@bp.route('/client/<int:client_id>', methods=['GET', 'PUT'])
@jwt_required()
def client_profile(client_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'trainer':
        return jsonify({"msg": "Access denied"}), 403
    
    client = Client.query.get(client_id)
    if not client:
        return jsonify({"msg": "Client not found"}), 404
    
    if request.method == 'GET':
        return jsonify({
            "id": client.id,
            "name": client.name,
            "age": client.age,
            "height": client.height,
            "weight": client.weight,
            "goals": client.goals
        }), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        client.name = data.get('name', client.name)
        client.age = data.get('age', client.age)
        client.height = data.get('height', client.height)
        client.weight = data.get('weight', client.weight)
        client.goals = data.get('goals', client.goals)
        db.session.commit()
        return jsonify({"msg": "Client profile updated successfully"}), 200

@bp.route('/client/<int:client_id>/diet', methods=['GET', 'PUT'])
@jwt_required()
def client_diet(client_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'trainer':
        return jsonify({"msg": "Access denied"}), 403
    
    diet_plan = DietPlan.query.filter_by(client_id=client_id).first()
    if not diet_plan:
        diet_plan = DietPlan(client_id=client_id)
        db.session.add(diet_plan)
    
    if request.method == 'GET':
        return jsonify({
            "breakfast": diet_plan.breakfast,
            "lunch": diet_plan.lunch,
            "dinner": diet_plan.dinner,
            "snacks": diet_plan.snacks
        }), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        diet_plan.breakfast = data.get('breakfast', diet_plan.breakfast)
        diet_plan.lunch = data.get('lunch', diet_plan.lunch)
        diet_plan.dinner = data.get('dinner', diet_plan.dinner)
        diet_plan.snacks = data.get('snacks', diet_plan.snacks)
        db.session.commit()
        return jsonify({"msg": "Diet plan updated successfully"}), 200