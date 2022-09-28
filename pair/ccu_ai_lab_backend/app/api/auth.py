from flask import jsonify, request, current_app, url_for, Blueprint, request, session
from flask_jwt_extended import (create_access_token, decode_token)
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.models.webinfo import Webinfo
from app.models.chat import Chat
from . import api, response
from .. import app, db, blacklist, mail
from .decorators import token_required
import datetime
import re
import random
import string

TOKEN_EXPIRES_DAYS = 7

# todo forgot password
   
@api.route("/auth/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    if not email:
        return response.error(403, "Missing email parameter")
    if not password:
        return response.error(403, "Missing password parameter")
    user = User.query.filter_by(email=email).first()
    if not user:
        return response.error(403, "User Not Found.")
    if not user.verify_password(password):
        return response.error(403, "User Password Error.")
    if user.blocked == True or user.confirmed == False:
        return response.error(403, "Invalid Account.")

    user.last_seen = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user.location = request.remote_addr
    db.session.commit()
    expires = datetime.timedelta(days=TOKEN_EXPIRES_DAYS)
    access_token = create_access_token(identity=email, expires_delta=expires)
        
    return response.success({"access_token": access_token, "user": user.to_json()})


@api.route("/auth/logout", methods=["DELETE"])
@token_required
def logout(f):
    token = request.headers["x-access-tokens"]
    data = decode_token(token)
    blacklist.add(data["jti"])
    return response.success()

# password need convert to sha256 in frontend


@api.route("/auth/register", methods=["POST"])
def register():
    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")
    confirm_password = request.json.get("confirm_password")
    role_id = request.json.get("role_id")

    # todo
    #  Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0,
    #            "Usernames must have only letters, numbers, dots or "
    #            "underscores")]
    if not role_id:
        return response.error(403, "Missing role_id parameter")
    if role_id < 1 or role_id > 3:
        return response.error(403, "Missing role_id error")
    if not email:
        return response.error(403, "Missing email parameter")
    if not username:
        return response.error(403, "Missing username parameter")
    if not password:
        return response.error(403, "Missing password parameter")
    if not confirm_password:
        return response.error(403, "Missing confirm_password parameter")
    if password != confirm_password:
        return response.error(403, "Password and Confirm Password Not Match")

    regex = '[^@]+@[^@]+\.[^@]+'
    if(re.search(regex, email)):
        print("Valid Email")
    else:
        return response.error(403, "Invalid Email")

    if User.query.filter_by(email=email.lower()).first():
        return response.error(403, "Email already registered")
    user = User(email=email, username=username, role_id=role_id, password=password, confirmed_email=email,
                confirmed=0, location=request.remote_addr, last_seen=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.session.add(user)
    db.session.commit()

    expires = datetime.timedelta(days=TOKEN_EXPIRES_DAYS)
    access_token = create_access_token(identity=email, expires_delta=expires)
    role = user.role.name

    new_user = User.query.filter_by(email=email.lower()).first()
    webinfos = Webinfo.query.get(1)
    # send mail
    subject = 'Confirm your account for Taiwan-India Professional Expertise and Organization Cooperation Platform'
    message = 'Hi ' + new_user.username + ', <br><br>' \
        'Thank you for registering with Taiwan-India Professional Expertise and Organization Cooperation Platform.<br>' \
        '<br>' \
        'Please click the following link to confirm your account:<br>' \
        'https://127.0.0.1/center/#/auth/confirmed/' + str(new_user.id) + '/' + new_user.confirmed_hash.replace("pbkdf2:sha256:50000$", '') + '<br>' \
        'You will able to login after the activation.<br>' \
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
        recipients=[new_user.email],
        html=message
    )
    mail.send(msg)

    return response.success({"access_token": access_token, "user": user.to_json()})


@api.route("/auth/resend", methods=["POST"])
def resend():
    email = request.json.get("email")

    if not email:
        return response.error(403, "Missing email parameter")
    regex = '[^@]+@[^@]+\.[^@]+'
    if(re.search(regex, email)):
        print("Valid Email")
    else:
        return response.error(403, "Invalid Email")
    if not User.query.filter_by(email=email.lower()).first():
        return response.error(403, "There is no such Email!")

    new_user = User.query.filter_by(email=email.lower()).first()
    webinfos = Webinfo.query.get(1)
    # send mail
    subject = 'Confirm your account for Taiwan-India Professional Expertise and Organization Cooperation Platform'
    message = 'Hi ' + new_user.username + ', <br><br>' \
        'Thank you for registering with Taiwan-India Professional Expertise and Organization Cooperation Platform.<br>' \
        '<br>' \
        'Please click the following link to confirm your account:<br>' \
        'https://127.0.0.1/center/#/auth/confirmed/' + str(new_user.id) + '/' + new_user.confirmed_hash.replace("pbkdf2:sha256:50000$", '') + '<br>' \
        'You will able to login after the activation.<br>' \
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
        recipients=[new_user.email],
        html=message
    )
    mail.send(msg)

    return response.success()

# confirmed_hash need convert to sha256 in frontend


@api.route("/auth/confirmed/", methods=["PUT", "PATCH"])
def confirmed():
    user_id = request.json.get("user_id")
    confirmed_hash = request.json.get("confirmed_hash")
    if not user_id:
        return response.error(403, "Missing User parameter")
    if not confirmed_hash:
        return response.error(403, "Missing Confirmed parameter")

    user = User.query.get(user_id)
    if not user.verify_confirmed_email(confirmed_hash):
        return response.error(403, "User Confirmed Error.")

    user.confirmed = 1
    db.session.commit()

    expires = datetime.timedelta(days=TOKEN_EXPIRES_DAYS)
    access_token = create_access_token(
        identity=user.email, expires_delta=expires)
    role = user.role.name

    return response.success({"access_token": access_token, "user": user.to_json()})


@api.route("/auth/change_password", methods=["PUT", "PATCH"])
@token_required
def change_password(f):
    password = request.json.get("password")
    new_password = request.json.get("new_password")
    confirm_password = request.json.get("confirm_password")
    if not password:
        return response.error(403, "Missing password parameter")
    if not new_password:
        return response.error(403, "Missing new_password parameter")
    if not confirm_password:
        return response.error(403, "Missing confirm_password parameter")
    if new_password != confirm_password:
        return response.error(403, "Password and Confirm Password Not Match")

    token = request.headers["x-access-tokens"]
    user_email = decode_token(token)['identity']
    user = User.query.filter_by(email=user_email).first()

    if not user:
        return response.error(403, "User Not found.")
    if not user.verify_password(password):
        return response.error(403, "User Passwod Error.")

    user.location = request.remote_addr
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return response.success()


@api.route("/auth/resetpassword", methods=["POST"])
def resetpassword():
    email = request.json.get("email")

    if not email:
        return response.error(403, "Missing email parameter")
    regex = '[^@]+@[^@]+\.[^@]+'
    if(re.search(regex, email)):
        print("Valid Email")
    else:
        return response.error(403, "Invalid Email")

    user = User.query.filter_by(email=email.lower()).first()
    if not User:
        return response.error(403, "There is no such Email!")

    new_password = ''.join(random.choice(string.ascii_letters + string.digits)
                           for x in range(16))  # Generate [0-9, a-z, A-Z] 16 words
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    new_user = User.query.filter_by(email=email.lower()).first()
    webinfos = Webinfo.query.get(1)
    # send mail
    subject = 'Your reset password for Taiwan-India Professional Expertise and Organization Cooperation Platform'
    message = 'Hi ' + new_user.username + ', <br><br>' \
        'Here is your reset password for Taiwan-India Professional Expertise and Organization Cooperation Platform.<br>' \
        '<br>' \
        'PASSWORD:' + new_password + '<br>' \
        '<br>' \
        'Please click the following link to login your account:<br>' \
        'https://127.0.0.1/center/#/login' \
        '<br>' \
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
        recipients=[new_user.email],
        html=message
    )
    mail.send(msg)

    return response.success()
