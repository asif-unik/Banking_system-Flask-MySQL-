from flask import request,Blueprint,jsonify,session,current_app,make_response
from app.md.models.user_model import User
from hashlib import sha256
from datetime import datetime, timezone, timedelta
import jwt
from app.auth import auth_bp




@auth_bp.route('/login',methods=['POST'])
def login():
    data = request.json
    id_in_session = session.get('id')
    if id_in_session:
        user = User.query.filter_by(name=data['name']).first()
        if id_in_session==user.id:
            return jsonify({"message":"You are already logged in.."})

    if not data:
        return jsonify({'message':"Login field can't be Empty..!!"})
    name = data['name']
    password = data['password']
    user = User.query.filter_by(name=name).first()
    if user and sha256(password.encode('utf-8')).hexdigest() == user.password:
        # set user_id in session
        session['id']=user.id

         # Generate JWT token
        expiry = datetime.now(timezone.utc) + timedelta(minutes=60)
        payload = {'id': user.id, 'email': user.email, 'exp': expiry}
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        # Create response with token as cookie
        response = make_response(jsonify({'message': 'Login Successful', 'token': token},{'id':user.id}))
        print("token: ",token)
        response.set_cookie('token', token, httponly=True)
        
        return response, 200

    return jsonify({"Message":"Invalid Credentials..."})
    