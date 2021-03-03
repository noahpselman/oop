from flask import Flask
from src.api.login import login


app = Flask(__name__)
app.register_blueprint(login, url_prefix='/user')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def go_to_login():
    return {""}
