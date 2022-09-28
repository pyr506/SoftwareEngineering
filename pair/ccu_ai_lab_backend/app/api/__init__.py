from flask import render_template, jsonify, request, current_app, url_for, Blueprint, Response
from werkzeug.exceptions import HTTPException
import json
api = Blueprint('api', __name__)

from . import chat, auth, news, events, users, response, research, settings, specific_periods, COPI_projects, webinfos, image_upload
from .. import app
from app.models.role import Role
from app.models.user import User
from app.models.research import Research
from app.models.setting import Setting

prod_mode = True

#@api.before_request
#def before_request():
    #if not request.is_json and request.method != 'GET':
    #    return response.error(403, "Content-Type Error. (only-accept: json)")
    #elif request.is_xhr and request.method == 'POST':
        #upload img pass
    #    print("img upload")

@app.after_request
def af_request(response):
    if "doc" not in request.url:
        if not prod_mode:
            response = Response(json.dumps(response.get_json()), mimetype='application/json')
        else:
            response = Response(response.get_data().decode("utf-8"), mimetype='application/json')

        # 允許跨域
        response.headers['Access-Control-Allow-Origin'] = '*'
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'POST, DELETE, PUT, GET, OPTIONS'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
    return response

@api.route('/doc', methods = ['GET'])
def render_doc():
    return render_template('doc.html')

@api.route('/initial', methods = ['GET'])
def initail():
    Role.initial()
    User.initial()
    Research.initial()
    Setting.initial()
    return response.success()

@api.app_errorhandler(400)
@api.app_errorhandler(403)
@api.app_errorhandler(404)
def error_4xx(error):
    print(str(error))
    if error.code == 404:
        return response.error(error.code, "Api Not Found.")
    elif "decode JSON object: Expecting value:" in str(error):
        return response.error(error.code, "Request Format Error. (Empty Json Object)")

    return response.error(error.code, str(error))

@api.app_errorhandler(Exception)
def handle_exception(error):
    print(str(error))
    return response.error(500, "Server Error.")