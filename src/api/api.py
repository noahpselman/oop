from flask import Flask, render_template
from src.api.user import user


app = Flask(__name__)
app.register_blueprint(user, url_prefix='/user')


@app.route('/api')
def index():
    return {"message": "Welcome to the university website"}


@app.route('/login', methods=['GET'])
def go_to_login():
    return {"message": "going to the login page"}