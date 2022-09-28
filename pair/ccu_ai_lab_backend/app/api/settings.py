from flask import jsonify, request, current_app, url_for
from . import api, response
from .. import app, db
from app.models.setting import Setting
from .decorators import token_required
from datetime import datetime, date

@api.route('/settings/<int:setting_id>', methods = ['GET'])
@token_required
def getSetting(f, setting_id):
    setting = Setting.query.get(setting_id)
    if not setting:
        return response.error(404, "Setting not found")

    return response.success(setting.to_json())

@api.route('/settings', methods = ['GET'])
@token_required
def getSpecificPeriods(f):
    settings = Setting.query.all()
    data = []
    for setting in settings:
        data.append(setting.to_json())
    return response.success(data)

@api.route('/settings', methods = ['POST'])
@token_required
def newSpecificPeriodResearch(current_user):
    key = request.json.get('key')
    value = request.json.get('value')
    if not key:
        return response.error(403, "Missing key parameter")
    elif not value:
        return response.error(403, "Missing value parameter")

    if Setting.query.filter_by(key=key).first():
        return response.error(403, "Setting already exsit.")

    setting = Setting(key=key, value=value)
    db.session.add(setting)
    db.session.commit()
    return response.success()

@api.route('/settings/<int:setting_id>', methods = ['PUT', 'PATCH'])
@token_required
def update_setting(current_user, setting_id):
    try:
        if not setting_id:
            return response.error(403, "Missing setting_id parameter")

        setting = Setting.query.get(setting_id)
        if not setting:
            return response.error(403, "Setting not found")

        if request.method in ['PUT','PATCH']:
            key = request.json.get('key')
            value = request.json.get('value')
            setting.key = key
            setting.value = value
            setting.updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            db.session.commit()
        else:
            db.session.delete(setting)

        db.session.commit()

    except Exception as e:
        print(str(e))
        if "Duplicate entry" in str(e):
            return response.error(403, "'%s' Already Exist." % name)
        else:
            return response.error(403, "Operation error.")

    return response.success()