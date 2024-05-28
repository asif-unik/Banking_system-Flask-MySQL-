from app.models.user_model import User
from app.models.transactions_model import Transaction
from app.serde.user_schema import userschema, user_list_schema
from flask import jsonify,request,Blueprint,session
from app.controllers.token import token_required


user_accounts_bp = Blueprint('user_accounts',__name__)

@user_accounts_bp.route('/user_accounts',methods=['GET'])
@token_required
def get():
    session_id = session.get('id')
    if not session_id:
        return jsonify({"Message":"Login Required..!"})
    if session_id:
        admin = User.query.get(session_id)
        if admin.is_admin:
            users = User.query.all()
            user_list = [{"Account_No.":user.id,"name":user.name,"email":user.email} for user in users if user.is_admin==0]
            return jsonify(user_list)
        return jsonify({"Message":"You are Not a authorised Employee."})
    return jsonify({'Message:"Invalid Credentials.'})
