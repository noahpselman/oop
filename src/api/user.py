from flask import Blueprint, request
from src.api.authentication.Authenticator import Authenticator

user = Blueprint('user', __name__)


@user.route('/auth')
def authenticate():
    username = request.args.get('username', '')
    # print(username)
    password = request.args.get('password', '')
    # print(password)
    auth = Authenticator.getInstance()
    result = auth.authenticate_user(username, password)
    return {"loginSuccess": result}
