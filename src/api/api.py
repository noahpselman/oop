from src.Logging.Logger import Logger
from src.Controllers.MainController import MainController
from flask import Flask, request


app = Flask(__name__)
controller = MainController.getInstance()
logger = Logger.getInstance()
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
        logger.log(context='Router', method='authenticate-post',
                   msg=f'Authentication endpoint hit with data {request.json}')
        # return {"the thing is": "something happened"}

        user_id = data.get('user_id', '')
        password = data.get('password', '')
        result = controller.login(user_id, password)
        response = {
            "loginSuccess": result
        }
        logger.log(context='Router', method='authenticate-post',
                   msg=f'Authentication with data {request.json} evaluated to {result}')
        return response
        # if result:
        #     response['loginSuccess'] = True

        #     entity = controller.setup_user(user_id)
        #     response['entityData'] = entity.jsonify()
        #     print(response)
        # else:
        #     response['loginSuccess'] = False

        # return response
        # return {'response': response}
        # return {"loginSuccess": {'another dict': 'with a value', "and a key": ['to a list']}}

    elif request.method == 'GET':
        pass
        return {"twas a get"}


@app.route('user', methods=['POST'])
def user():
    data = request.json
    logger.log(context='Router', method='user-post',
               msg=f'User endpoint hit with data {request.json}')
    user_id = data.user_id
    response = {}
    if data.loggedIn:
        entity = controller.setup_user(user_id)
        response['entityData'] = entity.jsonify()
        response['success'] = True
        logger.log(context='Router', method='user-post',
                   msg=f'User endpoint with data {request.json} returned entity data')
    else:
        response['success': False]
        logger.log(context='Router', method='user-post',
                   msg=f'User endpoint with data {request.json} failed')
    return response


@app.route('/search', methods=['GET'])
def search():
    print("search endpoint hit")

    logger.log(context='Router', method='search-get',
               msg=f'Search endpoint hit with args {request.args}')

    result = controller.search_for_course_section(request.args)
    response = {'resultsFound': bool(result)}
    if result:
        course_sections = [cs.jsonify() for cs in result]
        response['searchResult'] = course_sections
        logger.log(context='Router', method='search-get',
                   msg=f'Search endpoint hit with args {request.args} found result')
    return response


@app.route('/drop', methods=['POST'])
def drop():
    print("drop called with following data")
    data = request.json
    section_index = data['section_index']
    student_id = data['user_id']
    logger.log(context='Router', method='drop-post',
               msg=f'Drop endpoint hit with args {section_index}, {student_id}')
    result = controller.drop_course(
        user_id=user_id, section_index=section_index)
    response = {
        'report': result['report'],
        'entityData': result['student'].jsonify()
    }
    print("response", response)
    logger.log(context='Router', method='drop-post',
               msg=f'Drop endpoint with args {section_index}, {user_id} {response.report.success}')
    # section_ids = parse_section_index(data['section_index'])
    # print("section_index", section_ids)
    return response


@app.route('/register', methods=['POST'])
def register():
    print("register endpoint called")
    print("data", request.json)
    data = request.json
    section_index = data['section_index']
    student_id = data['user_id']
    logger.log(context='Router', method='register-post',
               msg=f'Register endpoint hit with args {section_index}, {student_id}')

    result = controller.register(
        student_id=student_id, section_index=section_index)
    response = {
        'report': result['report'],
        'entityData': result['student'].jsonify()
    }
    logger.log(context='Router', method='register-post',
               msg=f'Register endpoint with args {section_index}, {user_id} {response.report.success}')
    return response
