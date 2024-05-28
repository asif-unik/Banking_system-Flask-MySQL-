from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from hashlib import sha256
from app.models.user_model import User
from app.serde.user_schema import user_schema
from app import db


signup_bp = Blueprint('signups', __name__)
@signup_bp.route('/signup', methods=['POST'])
def post():
    data = request.json
    if not data.get('name'):
        return jsonify({'message':'name cannot be empty'})

    if not data:
        return jsonify({'message':'No data Provided'}), 400

    try:
        validated_data = user_schema().load(data)

    except ValidationError as e:
        return jsonify({'message':'Validation Error', 'errors':e.messages}), 400

    if User.query.filter_by(email=validated_data['email']).count():
        return jsonify({'message':'Email already registered Kindly login to continue'}), 409
    

    hashed_password = sha256(data['password'].encode('utf-8')).hexdigest()
    
    new_user = User(
        name=validated_data['name'],
        email=validated_data['email'],
        password=hashed_password,
        is_admin=validated_data['is_admin']
    )

    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message':'Signed Up Successfully'}), 200