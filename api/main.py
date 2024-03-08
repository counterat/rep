from flask import Blueprint, request
from models import *

api_bp = Blueprint('api', __name__)

@api_bp.route('/authenticate', methods=['POST', "GET"])
def auth_view():
    user_id = request.args.get('user_id')
    password = request.args.get('password')
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user.password == password:
            return 
    except:
        return 'Wrong user or password', 403

@api_bp.route('/result_for_case/<int:operationid>')
def endpoint(operationid):
    
    
    return 'Hello, API!'    