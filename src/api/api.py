from src.Controllers.MainController import MainController
from flask import Flask, request

app = Flask(__name__)
controller = MainController.getInstance()
# app.register_blueprint(user, url_prefix='/user')


@app.route('/api')
def index():
    return {"message": "Welcome to the university website"}


@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        print(request.json)
        data = request.json
        # return {"the thing is": "something happened"}

        user_id = data.get('user_id', '')
        password = data.get('password', '')
        result = controller.login(user_id, password)
        if result:
            data = controller.setup_user(user_id)
        return {"loginSuccess": data}

    elif request.method == 'GET':
        pass
        return {"twas a get"}
