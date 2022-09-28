from flask import jsonify, request, current_app, url_for
from . import api, response
from .. import app, db
from app.models.user import User
from app.models.research import Research
from .decorators import token_required
from datetime import datetime
from app.models.user_research import UserResearch
from app.models.role import Role
import re

@api.route('/users', methods = ['GET'])
@token_required
def get_users(f):
    users = User.query.all()
    data = []
    for user in users:
        data.append(user.to_json())
    return response.success(data)

@api.route('/users/<int:user_id>', methods = ['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return response.error(404, "User not found")

    return response.success(user.to_json())

@api.route('/users/<int:user_id>', methods = ['DELETE'])
@token_required
def blocked_user(f, user_id):
    user = User.query.get(user_id)
    blocked = request.json.get('blocked')
    if not user:
        return response.error(404, "User not found")
    if not blocked:
        return response.error(403, "Missing blocked parameter")

    user.blocked = blocked
    user.location = request.remote_addr
    user.updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    db.session.commit()
    return response.success()

@api.route('/users/<int:user_id>', methods = ['PUT', 'PATCH'])
@token_required
def update_user(f, user_id):
    try:
        if not user_id:
            return response.error(403, "Missing user_id parameter")

        user = User.query.filter_by(id=user_id).first()

        if not user:
            return response.error(403, "User not found")

        if request.method in ['PUT','PATCH']:
            email = request.json.get('email')
            if not email:
                return response.error(403, "Missing E-mail parameter")
            regex = '[^@]+@[^@]+\.[^@]+'
            if(re.search(regex,email)):  
                print("Valid Email")
            else:  
                return response.error(403, "Invalid Email")
            username = request.json.get('username')
            if not username:
                return response.error(403, "Missing Username parameter")
            first_name = request.json.get('first_name')
            last_name = request.json.get('last_name')
            country = request.json.get('country')
            company = request.json.get('company')
            job_title = request.json.get('job_title')
            about_me = request.json.get('about_me')
            blocked = request.json.get('blocked')
            confirmed = request.json.get('confirmed')
            researches = request.json.get('researches')
            researches_name = request.json.get('researches_name')

            #add new researches
            AllResearch = Research.query.all()
            AllResearch_name = []
            k=0
            for item in AllResearch:
                AllResearch_name.append(item.name)
            for research_name in researches_name:
                if research_name not in AllResearch_name:
                    #print('not find:', research_name)
                    #add new research
                    newResearch = Research(name=research_name)
                    db.session.add(newResearch)
                    db.session.commit()

                    #get new research ID
                    getNewResearch = Research.query.filter(Research.name==research_name).first()
                    researches[k] = getNewResearch.id
                k=k+1

            for original_research in user.user_researches:
                db.session.delete(original_research)

            for research_id in researches:
                ur = UserResearch(user_id=user.id,research_id=research_id)
                user.user_researches.append(ur)

            user.email = email
            user.username = username
            user.country = country
            user.first_name = first_name
            user.last_name = last_name
            user.company = company
            user.job_title = job_title
            user.about_me = about_me
            user.blocked = blocked
            user.confirmed = confirmed
            user.location = request.remote_addr
            user.updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            db.session.commit()
        else:
            User.query.filter_by(id=user_id).update({'blocked': True})

        db.session.commit()

    except Exception as e:
        print(str(e))
        if "Duplicate entry" in str(e):
            return response.error(403, "'%s' Already Exist." % name)
        else:
            return response.error(403, "Operation error.")

    return response.success()