from app.models.transactions_model import Transaction
from app.serde.transaction_schema import transaction_list_schema,transaction_schema
from app import db
from flask import Blueprint,request,session,jsonify
from app.controllers.token import token_required
from datetime import datetime
from app.models.user_model import User
import json


transaction_bp = Blueprint('transaction',__name__)

@transaction_bp.route('/transaction',methods=['POST'])
@token_required
def post():
    data = request.json
    debit = data.get('debit')
    credit = data.get('credit')
    id = session.get('id')
    print('id',id)
    user = User.query.filter_by(id=id).first()
    print(user)
    if id and user:
        if debit:
            if debit > user.balance:
                return jsonify({"Message":"Insufficient Funds."})
            user.balance-=debit
            transaction = Transaction(debit=debit,credit=credit,date=datetime.utcnow().date(),time=datetime.utcnow().time(),account_balance=user.balance,user_id=id)
            user_balance = User(balance=user.balance)
            db.session.add(transaction,user_balance)
            db.session.commit()
            return jsonify({"Message":"Debit Successfuly."})
        if credit:
            user.balance += credit
            transaction = Transaction(debit=debit,credit=credit,date=datetime.utcnow().date(),time=datetime.utcnow().time(),account_balance=user.balance,user_id=id)
            user_balance = User(balance=user.balance)
            db.session.add(transaction,user_balance)
            db.session.commit()
            return jsonify({"Message":"Credited Successfuly."})
    elif not id:
        return jsonify({"Message":"Please Login First."})

    return jsonify({"Message":"Invalid login credentials"})

@token_required
@transaction_bp.route('/transaction/<int:id>',methods=['GET'])
def get(id):
    session_id=session.get('id')
    if not session_id:
        return jsonify({"Message":"Login Required..!"})
    if id == session_id:
        transactions = Transaction.query.filter_by(user_id=id)
        print('tran: ',transactions)
        return transaction_list_schema.dump(transactions)

    return jsonify({"Message":"Provide Valid Id"})
    print('get:',id)


