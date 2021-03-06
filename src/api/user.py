from flask import Blueprint, request
from src.Controllers.MainController import MainController

user = Blueprint('user', __name__)
controller = MainController.getInstance()



@user.route('/auth', methods = ['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        print(request.json)
        data = request.json
        # return {"the thing is": "something happened"}

        user_id = data.get('user_id', '')
        password = data.get('password', '')
        result = controller.login(user_id, password)
        if result:
            entity = controller.setup_user(user_id)
        return {"loginSuccess": result}

    elif request.method == 'GET':
        pass
        return {"twas a get"}
    # print(username)
    # print(password)
