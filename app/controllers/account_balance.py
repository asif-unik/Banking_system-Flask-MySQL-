from flask import Blueprint


account_balance_bp = Blueprint('account_balance',__name__)

@account_balance_bp('/account_balance',methods=['GET'])
def get():
    