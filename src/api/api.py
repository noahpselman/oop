from flask import Flask, request
from src.Controllers.MainController import MainController
from src.Logging.Logger import Logger
from src.util import get_current_quarter, parse_section_index

app = Flask(__name__)
controller = MainController.getInstance()
logger = Logger.getInstance()


@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
    response = {}
    if request.method == 'POST':
        print(request.json)
        data = request.json
        # logger.log(context='Router', method='authenticate-post',
        #            msg=f'Authentication endpoint hit with data {request.json}')
        # return {"the thing is": "something happened"}

        user_id = data.get('user_id', '')
        password = data.get('password', '')
        result = controller.login(user_id, password)
        print("result from auth", result)
        response = {
            "loginSuccess": result
        }
        print("response:", response)

        # logger.log(context='Router', method='authenticate-post',
        #            msg=f'Authentication with data {request.json} evaluated to {result}')
        return response

    elif request.method == 'GET':
        pass
        return {"twas a get"}


@app.route('/user', methods=['POST'])
def user():
    data = request.json
    # logger.log(context='Router', method='user-post',
    #            msg=f'User endpoint hit with data {request.json}')
    user_id = data['user_id']
    response = {}
    if data['logged_in']:
        entity = controller.setup_user(user_id)
        response['currentQuarter'] = get_current_quarter()
        response['entityData'] = entity.jsonify()
        response['displayCourses'] = response['entityData']['current_courses']
        response['success'] = True
        # logger.log(context='Router', method='user-post',
        #            msg=f'User endpoint with data {request.json} returned entity data')
    else:
        response['success'] = False
        # logger.log(context='Router', method='user-post',
        #            msg=f'User endpoint with data {request.json} failed')
    return response


@app.route('/currentcourses', methods=['POST'])
def currentcourses():
    data = request.json
    print("data from current course", data)
    student_id = data['student_id']
    quarter = data['quarter']

    result = controller.get_current_courses(
        student_id=student_id, quarter=quarter)

    response = {
        'student': result['student'].jsonify(),
        'courses': [r.jsonify() for r in result['courses']]
    }
    print(response)

    return response


@app.route('/search', methods=['GET'])
def search():
    print("search endpoint hit")
    print(request.args)

    # logger.log(context='Router', method='search-get',
    #    msg=f'Search endpoint hit with args {request.args}')

    result = controller.search_for_course_section(request.args)
    response = {'resultsFound': bool(result)}
    if result:
        course_sections = [cs.jsonify() for cs in result]
        response['searchResult'] = course_sections
    print("search response", response)
    # logger.log(context='Router', method='search-get',
    #            msg=f'Search endpoint hit with args {request.args} found result')
    return response


@app.route('/drop', methods=['POST'])
def drop():
    print("drop called with following data")
    data = request.json
    section_index = data['section_index']
    student_id = data['user_id']
    # logger.log(context='Router', method='drop-post',
    #            msg=f'Drop endpoint hit with args {section_index}, {student_id}')
    result = controller.drop_course(
        student_id=student_id, section_index=section_index)
    response = {
        'report': result['report'].jsonify(),
        'entityData': result['student'].jsonify()

    }
    print("response", response)
    # logger.log(context='Router', method='drop-post',
    #            msg=f'Drop endpoint with args {section_index}, {user_id} {response.report.success}')
    # section_ids = parse_section_index(data['section_index'])
    # print("section_index", section_ids)
    return response


@app.route('/register', methods=['POST'])
def register():
    print("register endpoint called")
    print("data", request.json)
    data = request.json
    section_index = data['section_index']
    parsed_index = parse_section_index(section_index)
    student_id = data['user_id']
    # logger.log(context='Router', method='register-post',
    #            msg=f'Register endpoint hit with args {section_index}, {student_id}')

    result = controller.register(
        student_id=student_id, section_index=section_index)
    response = {
        'report': result['report'].jsonify(),
        'entityData': result['student'].jsonify(),
        'searchType': result['search_type'],
        'searchResult': [cs.jsonify() for cs in result['search_results']],
        'currentQuarter': parsed_index['quarter']
    }

    # logger.log(context='Router', method='register-post',
    #            msg=f'Register endpoint with args {section_index}, {user_id} {response.report.success}')
    return response


@app.route('/lab', methods=['POST'])
def lab():
    data = request.json
    print("data from lab endpoint", data)
    section_index = data['section_index']
    parsed_index = parse_section_index(section_index)
    lab_index = data['lab_index']
    student_id = data['student_id']
    result = controller.register_for_lab(
        student_id=student_id, section_index=section_index, lab_index=lab_index)
    response = {
        'report': result['report'].jsonify(),
        'entityData': result['student'].jsonify(),
        'searchType': result['search_type'],
        'searchResult': [cs.jsonify() for cs in result['search_results']],
        'currentQuarter': parsed_index['quarter']}
    return response


@ app.route('/permission', methods=['POST'])
def permission():
    print("permission endpoint hit")
    data = request.json
    section_index = data['section_index']
    student_id = data['student_id']
    permission_type = data['permission_type']

    result = controller.request_permission(
        permission_type=permission_type, student_id=student_id, section_index=section_index)

    return {'success': result}
