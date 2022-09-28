from flask import jsonify
import json
from . import api
from .. import app

def error(code, message):
    response = jsonify({'status': 'error', 'message': message})
    response.status_code = code
    return response

def success(data=None):
    result = {
        'status': 'success'
    }
    if data is not None:
        result['data'] = data
    response = jsonify(result)
    response.status_code = 200
    return response