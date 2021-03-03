from flask import Blueprint

user = Blueprint('user', __name__)


@user.route('/auth')
def authenticate():
    return {"auth_success": True}
