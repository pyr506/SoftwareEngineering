from flask import jsonify, request, current_app, url_for
from . import api, response
from .. import app, db
from app.models.specific_period import SpecificPeriod
from app.models.COPI_project import COPI_project
from app.models.setting import Setting
from .decorators import token_required, in_speific_period_time
from datetime import datetime, date
from app.models.user_research import UserResearch
from app.models.role import Role
from app.models.research import Research
from app.models.specific_period_research import SpecificPeriodResearch
import json
from sqlalchemy import distinct
import validators

@api.route('/specific_periods/field/matchmaking', methods = ['GET'])
@token_required
@in_speific_period_time
def get_specific_period_match_field(start, end, current_user):
    user_prefer_researches = []
    # get user prefer researches field
    for user_research in current_user.user_researches:
        user_prefer_researches.append(user_research.research_id)

    specific_period_result = SpecificPeriodResearch.query.with_entities(SpecificPeriodResearch.specific_period_id).distinct().filter(SpecificPeriodResearch.created_at <= end).filter(SpecificPeriodResearch.created_at >= start).filter(SpecificPeriodResearch.research_id.in_(user_prefer_researches))
    specific_periods = SpecificPeriod.query.filter(SpecificPeriod.id.in_(specific_period_result))
    data = []
    for specific_period in specific_periods:
        data.append(specific_period.to_json())

    return response.success(data)

@api.route('/specific_periods/name/matchmaking', methods = ['GET'])
@token_required
@in_speific_period_time
def get_specific_period_match_name(start, end, current_user):
    project_title = request.json.get('project_title')
    if not project_title:
        return response.error(403, 'Missing project_title parameter')
    keyword = "%{}%".format(project_title)
    specific_periods = SpecificPeriod.query.filter(SpecificPeriod.created_at <= end).filter(SpecificPeriod.created_at >= start).filter(SpecificPeriod.project_title.like(keyword)).all()

    data = []
    for specific_period in specific_periods:
        data.append(specific_period.to_json())

    return response.success(data)


@api.route('/specific_periods/<int:specific_period_id>', methods = ['GET'])
@token_required
@in_speific_period_time
def get_specific_period(start, end, current_user, specific_period_id):
    specific_period = SpecificPeriod.query.get(specific_period_id)
    if not specific_period:
        return response.error(404, 'Specific Period Research not found')

    return response.success(specific_period.to_json())

@api.route('/specific_periods', methods = ['GET'])
@token_required
@in_speific_period_time
def get_specific_periods(start, end, current_user):
    specific_periods = SpecificPeriod.query.all()
    data = []
    for specific_period in specific_periods:
        data.append(specific_period.to_json())

    return response.success(data)

@api.route('/specific_periods/myCOPIproject', methods = ['GET'])
@token_required
@in_speific_period_time
def get_my_COPI_specific_periods(start, end, current_user):
    specific_periods = SpecificPeriod.query.join(COPI_project, SpecificPeriod.id==COPI_project.specific_period_id).filter(COPI_project.user_id==current_user.id)
    data = []
    for specific_period in specific_periods:
        data.append(specific_period.to_json())
    return response.success(data)

@api.route('/specific_periods/myproject', methods = ['GET'])
@token_required
@in_speific_period_time
def get_my_specific_periods(start, end, current_user):
    specific_periods = SpecificPeriod.query.filter(SpecificPeriod.user_id == current_user.id)
    data = []
    for specific_period in specific_periods:
        data.append(specific_period.to_json())
    return response.success(data)

@api.route('/specific_periods/interesting_project', methods = ['GET'])
@token_required
@in_speific_period_time
def get_interesing_specific_periods(start, end, current_user):

    # get user prefer researches field
    USR = UserResearch.query.filter(UserResearch.user_id==current_user.id).with_entities(UserResearch.research_id)
    specific_periods = SpecificPeriod.query.join(SpecificPeriodResearch, SpecificPeriod.id==SpecificPeriodResearch.specific_period_id).filter(SpecificPeriod.user_id!=current_user.id).filter(SpecificPeriodResearch.research_id.in_((USR))).all()
    
    data = []
    for specific_period in specific_periods:
        data.append(specific_period.to_json())
    return response.success(data)

@api.route('/specific_periods', methods = ['POST'])
@token_required
@in_speific_period_time
def new_specific_period_research(start, end, current_user):
    dateformat = '%Y-%m-%d'
    try:
        user_id = current_user.id
        if not user_id:
            return response.error(403, "Missing User parameter")
        name_of_pi = request.json.get('name_of_pi')
        if not name_of_pi:
            return response.error(403, "Missing Name of PI parameter")
        country = request.json.get('country')
        if not country:
            return response.error(403, "Missing Country parameter")
        university = request.json.get('university')
        if not university:
            return response.error(403, "Missing University parameter")
        department = request.json.get('department')
        if not department:
            return response.error(403, "Missing Department parameter")
        project_title = request.json.get('project_title')
        if not project_title:
            return response.error(403, "Missing Project Title parameter")
        link = request.json.get('link')
        if not link:
            return response.error(403, "Missing Link parameter")
        valid=validators.url(link)
        if valid==True:
            print("Url is valid")
        else:
            return response.error(403, "Invalid Link")
        start_date = request.json.get('start_date')
        start_date = start_date[:10]
        datetime.strptime(start_date, dateformat)
        if not start_date:
            return response.error(403, "Missing Start Date parameter")
        end_date = request.json.get('end_date')
        end_date = end_date[:10]
        datetime.strptime(end_date, dateformat)
        if not end_date:
            return response.error(403, "Missing End Date parameter")
        if start_date>end_date:
            return response.error(403, "Start Date must be less then End Date")
        apply_copi_end_date = request.json.get('apply_copi_end_date')
        apply_copi_end_date = apply_copi_end_date[:10]
        datetime.strptime(apply_copi_end_date, dateformat)
        if not apply_copi_end_date:
            return response.error(403, "Missing CO-PI End Date parameter")
        project_content = request.json.get('project_content')
        if not project_content:
            return response.error(403, "Missing Project Content parameter")
        
        researches = request.json.get('researches')
        researches_name = request.json.get('researches_name')
        if not researches:
            return response.error(403, 'Missing Fields parameter')
        elif len(researches) < 1:
            return response.error(403, 'At least 1 Field')
        specific_period = SpecificPeriod(user_id=user_id,country=country,university=university, \
        start_date=start_date, end_date=end_date, \
        name_of_pi=name_of_pi,department=department,project_title=project_title,link=link, \
        apply_copi_end_date=apply_copi_end_date, project_content=project_content,
        location=request.remote_addr)

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

        for research_id in researches:
            spr = SpecificPeriodResearch(research_id=research_id)
            specific_period.specific_period_researches.append(spr)

        db.session.add(specific_period)
        db.session.commit()

        return response.success()
    except Exception as e:
        print(str(e))
        return response.error(403, e)

@api.route('/specific_periods/<int:specific_period_id>', methods = ['PUT', 'PATCH', 'DELETE'])
@token_required
@in_speific_period_time
def update_specific_period(start, end, current_user, specific_period_id):
    try:
        dateformat = '%Y-%m-%d'
        if not specific_period_id:
            return response.error(403, 'Missing specific_period_id parameter')

        specific_period = SpecificPeriod.query.get(specific_period_id)

        if request.method in ['PUT','PATCH']:
            user_id = current_user.id
            if not user_id:
                return response.error(403, "Missing User parameter")
            country = request.json.get('country')
            if not country:
                return response.error(403, "Missing Country parameter")
            university = request.json.get('university')
            if not university:
                return response.error(403, "Missing University parameter")
            name_of_pi = request.json.get('name_of_pi')
            if not name_of_pi:
                return response.error(403, "Missing Name of PI parameter")
            department = request.json.get('department')
            if not department:
                return response.error(403, "Missing Department parameter")
            start_date = request.json.get('start_date')
            start_date = start_date[:10]
            datetime.strptime(start_date, dateformat)
            if not start_date:
                return response.error(403, "Missing Start Date parameter")
            end_date = request.json.get('end_date')
            end_date = end_date[:10]
            datetime.strptime(end_date, dateformat)
            if not end_date:
                return response.error(403, "Missing End Date parameter")
            if start_date>end_date:
                return response.error(403, "Start Date must be less then End Date")
            project_title = request.json.get('project_title')
            if not project_title:
                return response.error(403, "Missing Project Title parameter")
            link = request.json.get('link')
            if not link:
                return response.error(403, "Missing Link parameter")
            valid=validators.url(link)
            if valid==True:
                print("Url is valid")
            else:
                return response.error(403, "Invalid Link")
            apply_copi_end_date = request.json.get('apply_copi_end_date')
            apply_copi_end_date = apply_copi_end_date[:10]
            datetime.strptime(apply_copi_end_date, dateformat)
            if not apply_copi_end_date:
                return response.error(403, "Missing CO-PI End Date parameter")
            project_content = request.json.get('project_content')
            if not project_content:
                return response.error(403, "Missing Project Content parameter")
            
            researches = request.json.get('researches')
            researches_name = request.json.get('researches_name')
            if not researches:
                return response.error(403, 'Missing Fields parameter')
            elif len(researches) < 1:
                return response.error(403, 'At least 1 Field')
            
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
                    
            for original_research in specific_period.specific_period_researches:
                db.session.delete(original_research)

            for research_id in researches:
                spr = SpecificPeriodResearch(research_id=research_id)
                specific_period.specific_period_researches.append(spr)

            
            specific_period.user_id = user_id
            specific_period.country = country
            specific_period.university = university
            specific_period.name_of_pi = name_of_pi
            specific_period.department = department
            specific_period.start_date = start_date
            specific_period.end_date = end_date
            specific_period.project_title = project_title
            specific_period.link = link
            specific_period.project_content=project_content
            specific_period.apply_copi_end_date=apply_copi_end_date
            specific_period.location = request.remote_addr
            specific_period.updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            db.session.commit()
        else:
            db.session.delete(specific_period)

        db.session.commit()
        return response.success()

    except Exception as e:
        print(str(e))
        if 'Duplicate entry' in str(e):
            return response.error(403, 'Already Exist.')
        else:
            return response.error(403, 'Operation error.')