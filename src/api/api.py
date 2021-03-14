from src.Controllers.MainController import MainController
from flask import Flask, request

app = Flask(__name__)
controller = MainController.getInstance()
controller.setup_db()
# app.register_blueprint(user, url_prefix='/user')


@app.route('/api')
def index():
    return {"message": "Welcome to the university website"}


@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
    response = {}
    if request.method == 'POST':
        print(request.json)
        data = request.json
        # return {"the thing is": "something happened"}

        user_id = data.get('user_id', '')
        password = data.get('password', '')
        result = controller.login(user_id, password)

        if result:
            response['loginSuccess'] = True

            entity = controller.setup_user(user_id)
            response['entityData'] = entity.jsonify()
            print(response)
        else:
            response['loginSuccess'] = False

        return response
        # return {'response': response}
        # return {"loginSuccess": {'another dict': 'with a value', "and a key": ['to a list']}}

    elif request.method == 'GET':
        pass
        return {"twas a get"}


@app.route('/search', methods=['GET'])
def search():
    print("search endpoint hit")
    print("search args", request.args)

    result = controller.search_for_course_section(request.args)
    response = {'resultsFound': bool(result)}
    if result:
        course_sections = [cs.jsonify() for cs in result]
        response['searchResult'] = course_sections
    print("search result", course_sections)
    return response


@app.route('/drop', methods=['POST'])
def drop():
    print("drop called with following data")
    data = request.json
    result = controller.drop_course(data)
    response = {
        'report': result['report'],
        'entityData': result['student'].jsonify()
    }
    print("response", response)
    # section_ids = parse_section_index(data['section_index'])
    # print("section_index", section_ids)
    return response


@app.route('/register', methods=['POST'])
def register():
    print("register endpoint called")
    print("data", request.json)
    data = request.json
    result = controller.register(data)
    response = {
        'report': result['report'],
        'entityData': result['student'].jsonify()
    }
    return response
