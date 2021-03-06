from flask import Flask, render_template
from src.api.user import user


app = Flask(__name__)
app.register_blueprint(user, url_prefix='/user')


@app.route('/api')
def index():
    return {"message": "Welcome to the university website"}


