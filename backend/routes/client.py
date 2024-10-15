from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Client, DietPlan, MealLog
from app import db
from datetime import datetime

bp = Blueprint('client', __name__)

@bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    current_user = User.query.get(get_jwt_identity())
    client = Client.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'GET':
        return jsonify({
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
        return jsonify({"msg": "Profile updated successfully"}), 200

@bp.route('/diet-plan', methods=['GET'])
@jwt_required()
def diet_plan():
    current_user = User.query.get(get_jwt_identity())
    client = Client.query.filter_by(user_id=current_user.id).first()
    diet_plan = DietPlan.query.filter_by(client_id=client.id).first()
    
    if not diet_plan:
        return jsonify({"msg": "No diet plan found"}), 404
    
    return jsonify({
        "breakfast": diet_plan.breakfast,
        "lunch": diet_plan.lunch,
        "dinner": diet_plan.dinner,
        "snacks": diet_plan.snacks
    }), 200

@bp.route('/meal-log', methods=['GET', 'POST'])
@jwt_required()
def meal_log():
    current_user = User.query.get(get_jwt_identity())
    client = Client.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'GET':
        logs = MealLog.query.filter_by(client_id=client.id).order_by(MealLog.date.desc()).limit(10).all()
        return jsonify([{
            "date": log.date.strftime('%Y-%m-%d'),
            "meal_type": log.meal_type,
            "food": log.food
        } for log in logs]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        new_log = MealLog(
            client_id=client.id,
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            meal_type=data['meal_type'],
            food=data['food']
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"msg": "Meal log added successfully"}), 201