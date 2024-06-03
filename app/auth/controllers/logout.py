from flask import Blueprint,jsonify,session,make_response, redirect,url_for, render_template
from app.auth import auth_bp



@auth_bp.route('/logout',methods=['GET'])
def logout():
    if 'id' not in session:
        return jsonify({'Message':'Please Login first..'})
    response = make_response(render_template('index.html'))
    response.set_cookie('token', '', expires=0)
    
    # Clear the session data
    session.pop('id')
    print(session)
    return response, 200

# return redirect(url_for('transaction.debit_funds'))