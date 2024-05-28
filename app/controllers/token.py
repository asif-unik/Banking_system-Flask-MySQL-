from functools import wraps
from flask import request, jsonify, session,current_app
import jwt


def token_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')

        if not token:
            return {'error':'Token is missing'}, 401
        
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            print("payload: ",payload)
            user_id = payload['id']

        except jwt.ExpiredSignatureError:
            return {'message':'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'message':'Invalid token'}, 401
        
        return func(*args, **kwargs)
    
    return decorated_function