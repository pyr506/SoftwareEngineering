from flask import jsonify, request, g, url_for, current_app
from . import api, response
from .. import app, db
from app.models.webinfo import Webinfo
from .decorators import token_required
from datetime import datetime

@api.route('/webinfos', methods = ['GET'])
def get_webinfos():
    webinfos = Webinfo.query.get(1)
    return response.success(webinfos.to_json())

@api.route('/webinfos', methods = ['PUT', 'PATCH', 'DELETE'])
@token_required
def update_webinfos(f):
    try:
        webinfos = Webinfo.query.get(1)

        if not webinfos:
            return response.error(403, "Webinfos not found")

        if request.method in ['PUT','PATCH']:
            tel = request.json.get('tel')
            if not tel:
                return response.error(403, "Missing tel parameter")
            email = request.json.get('email')
            if not email:
                return response.error(403, "Missing e-mail parameter")
            address = request.json.get('address')
            if not address:
                return response.error(403, "Missing address parameter")
            
            webinfos.tel = tel
            webinfos.email = email
            webinfos.address = address
        else:
            db.session.delete(webinfos)
        db.session.commit()
        return response.success()

    except Exception as e:
        print("error")
        print(str(e))
        return response.error(403, "Operation error.")