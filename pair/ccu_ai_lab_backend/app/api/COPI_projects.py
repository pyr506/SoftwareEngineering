from flask import jsonify, request, g, url_for, current_app
from . import api, response
from .. import app, db, mail
from flask_mail import Mail, Message
from app.models.user import User
from app.models.specific_period import SpecificPeriod
from app.models.COPI_project import COPI_project
from app.models.webinfo import Webinfo
from .decorators import token_required
from datetime import datetime


@api.route('/COPI_projects/<int:project_id>', methods=['GET'])
def get_COPI_projects(project_id):
    #COPIs = COPI_project.query.filter_by(specific_period_id=project_id).join(User)
    COPIs = COPI_project.query.filter_by(specific_period_id=project_id)
    data = []
    for COPI in COPIs:
        data.append(COPI.to_json())
    return response.success(data)

# @api.route('/COPI_projects/<int:post_id>', methods = ['GET'])
# def get_post(post_id):
#    post = Post.query.get(post_id)
#    if not post:
#        return response.error(404, "Post not found")
#    post.clicked = post.clicked + 1
#    db.session.commit()
#    return response.success(post.to_json())


@api.route('/COPI_projects', methods=['POST'])
@token_required
def new_COPI_project(f):
    specific_period_id = request.json.get('project_id')
    COPI_project_content = request.json.get('COPI_project_content')
    if not specific_period_id:
        return response.error(403, "Missing specific_period_id parameter")
    if not COPI_project_content:
        return response.error(403, "Missing COPI_project_content parameter")
    try:
        COPIproject = COPI_project(
            specific_period_id=specific_period_id, user_id=f.id, COPI_content=COPI_project_content)
        db.session.add(COPIproject)
        db.session.commit()

        # send mail
        SP = SpecificPeriod.query.get(COPIproject.specific_period_id)
        US = User.query.get(SP.user_id)
        COUS = User.query.get(COPIproject.user_id)
        webinfos = Webinfo.query.get(1)
        subject = 'Someone applied for Co-PI for your project.'
        message = 'Hi ' + US.username + ', <br><br>' \
            'This is to kindly notify you that the following user has submitted an application for Co-PI to your project "' + SP.project_title + '" for possible future cooperation.<br>' \
            '<br>' \
            'Applying User: ' + COUS.username + '<br>' \
            'Applying Content: ' + COPIproject.COPI_content + '<br>' \
            '<br>' \
            'Please check the following link for more information:<br>' \
            '<a href="https://127.0.0.1/center/#/projects/' + str(COPIproject.specific_period_id) + '">' + SP.project_title + '</a> <br>' \
            '<br>' \
            'best regards,<br>' \
            '---<br>' \
            'Taiwan-India Professional Expertise and Organization Cooperation Platform<br>' \
            'tel:' + webinfos.tel + '<br>' \
            'e-mail:' + webinfos.email+'<br>' \
            'address:' + webinfos.address + '<br>' \
            'web:' + webinfos.link + '<br>'
        msg = Message(
            subject=subject,
            recipients=[US.email],
            html=message
        )
        mail.send(msg)

        return response.success()

    except Exception as err:
        print(str(err))
        if "Duplicate entry" in str(err):
            return response.error(403, "'%s' Already Exist." % name)
        else:
            return response.error(403, "Operation error.")

# @api.route('/posts/<int:post_id>', methods = ['PUT', 'PATCH', 'DELETE'])
# @token_required
# def update_post(f, post_id):
#     try:
#         if not post_id:
#             return response.error(403, "Missing post_id parameter")

#         post = Post.query.filter_by(id=post_id).first()

#         if not post:
#             return response.error(403, "Post not found")

#         if request.method in ['PUT','PATCH']:
#             title = request.json.get('title')
#             post_type = request.json.get('post_type')
#             content = request.json.get('content')
#             if not title:
#                 return response.error(403, "Missing title parameter")
#             if post_type == None:
#                 return response.error(403, "Missing post_type parameter")
#             if not content:
#                 return response.error(403, "Missing content parameter")
#             post.title = title
#             post.post_type = post_type
#             post.content = content
#             post.location = request.remote_addr
#             post.updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
#         else:
#             db.session.delete(post)
#         db.session.commit()

#     except Exception as e:
#         print("error")
#         print(str(e))
#         return response.error(403, "Operation error.")

#     return response.success()


@api.route('/COPI_projects/<int:COPI_id>', methods=['PUT', 'PATCH'])
@token_required
def update_COPI_Accpted(f, COPI_id):
    try:
        if not COPI_id:
            return response.error(403, "Missing COPI_id parameter")

        COPI = COPI_project.query.filter_by(id=COPI_id).first()

        if not COPI:
            return response.error(403, "COPI not found")

        accepted = request.json.get('accepted')

        original_accepted = COPI.accepted
        COPI.accepted = accepted
        COPI.updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()

        # send mail
        if (not original_accepted) and accepted:
            US = User.query.get(COPI.user_id)
            SP = SpecificPeriod.query.get(COPI.specific_period_id)
            webinfos = Webinfo.query.get(1)
            subject = 'Your apply has been accepted.'
            message = 'Hi ' + US.username + ', <br><br>' \
                'Your application for CO-PI for the Project titled "' + SP.project_title + '" has been accepted.<br>' \
                'Please check the following link for more information:<br>' \
                '<a href="https://127.0.0.1/center/#/projects/' + str(COPI.specific_period_id) + '">' + SP.project_title + '</a><br>' \
                '<br>' \
                'best regards,<br>' \
                '---<br>' \
                'Taiwan-India Professional Expertise and Organization Cooperation Platform<br>' \
                'tel:' + webinfos.tel + '<br>' \
                'e-mail:' + webinfos.email+'<br>' \
                'address:' + webinfos.address + '<br>' \
                'web:' + webinfos.link + '<br>'
            msg = Message(
                subject=subject,
                recipients=[US.email],
                html=message
            )
            mail.send(msg)
        return response.success()

    except Exception as e:
        print("error")
        print(str(e))
        return response.error(403, "Operation error.")
