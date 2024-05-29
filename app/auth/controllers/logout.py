from flask import Blueprint,jsonify,session,make_response
from app.auth import auth_bp



@auth_bp.route('/logout',methods=['POST'])
def logout():
    if 'id' not in session:
        return jsonify({'Message':'Please Login first..'})
    response = make_response(jsonify({'message': 'Successfully logged out'}))
    response.set_cookie('token', '', expires=0)
    
    # Clear the session data
    session.pop('id')

    return response, 200
