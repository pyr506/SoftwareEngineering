from flask import jsonify, request, current_app, url_for
from . import api, response
from .. import app, db
from app.models.research import Research
from datetime import datetime
from .decorators import token_required
from sqlalchemy import exc

@api.route('/researches', methods = ['GET'])
def get_researches():
    researches = Research.query.all()
    data = []
    for research in researches:
        data.append(research.to_json())
    return response.success(data)

@api.route('/researches/<int:research_id>', methods = ['GET'])
def get_research(research_id):
    research = Research.query.get(research_id)
    if not research:
        return response.error(404, "Research not found")

    return response.success(research.to_json())

@api.route('/researches', methods = ['POST'])
@token_required
def create_research(f):
    name = request.json.get('name')
    if not name:
        return response.error(403, "Missing name parameter")

    try:
        research = Research(name = name)
        db.session.add(research)
        db.session.commit()
    except exc.IntegrityError as err:
        print(str(err))
        if "Duplicate entry" in str(err):
            return response.error(403, "'%s' Already Exist." % name)
        else:
            return response.error(403, "Operation error.")
    return response.success()

@api.route('/researches/<int:research_id>', methods = ['PUT', 'PATCH', 'DELETE'])
@token_required
def update_research(f, research_id):
    try:
        if not research_id:
            return response.error(403, "Missing research_id parameter")

        research = Research.query.filter_by(id=research_id).first()

        if not research:
            return response.error(403, "Research not found")

        if request.method in ['PUT','PATCH']:
            name = request.json.get('name')
            if not name:
                return response.error(403, "Missing name parameter")

            Research.query.filter_by(id=research_id).update({'name':  name, "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")})
        else:
            db.session.delete(research)

        db.session.commit()

    except exc.IntegrityError as err:
        print(str(err))
        if "Duplicate entry" in str(err):
            return response.error(403, "'%s' Already Exist." % name)
        else:
            return response.error(403, "Operation error.")
    return response.success()



