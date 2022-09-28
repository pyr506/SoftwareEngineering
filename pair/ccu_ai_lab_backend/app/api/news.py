from flask import jsonify, request, g, url_for, current_app
from . import api, response
from .. import app, db
from app.models.new import News
from app.models.user import User
from .decorators import token_required
from datetime import datetime

@api.route('/news', methods = ['GET'])
def get_news():
    news = News.query.all()
    data = []
    for new in news:
        data.append(new.to_json())
    return response.success(data)

@api.route('/news/<int:news_id>', methods = ['GET'])
def get_new(news_id):
    new = News.query.get(news_id)
    if not new:
        return response.error(404, "News not found")
    new.clicked = new.clicked + 1
    db.session.commit()

    return response.success(new.to_json())


@api.route('/news', methods = ['POST'])
@token_required
def create_new(f):
    title = request.json.get('title')
    content = request.json.get('content')
    if not title:
        return response.error(403, "Missing Title parameter")
    if not content:
        return response.error(403, "Missing Content parameter")
    try:
        new = News(title=title, content=content, user_id=f.id, location=request.remote_addr)
        db.session.add(new)
        db.session.commit()
        return response.success()
    except Exception as err:
        print(str(err))
        if "Duplicate entry" in str(err):
            return response.error(403, "'%s' Already Exist." % name)
        else:
            return response.error(403, "Operation error.")
    

@api.route('/news/<int:news_id>', methods = ['PUT', 'PATCH', 'DELETE'])
@token_required
def update_new(f, news_id):
    try:
        if not news_id:
            return response.error(403, "Missing news_id parameter")

        new = News.query.filter_by(id=news_id).first()

        if not new:
            return response.error(403, "News not found")

        if request.method in ['PUT','PATCH']:
            title = request.json.get('title')
            content = request.json.get('content')
            if not title:
                return response.error(403, "Missing Title parameter")
            if not content:
                return response.error(403, "Missing Content parameter")
            new.title = title
            new.content = content
            new.location = request.remote_addr
            new.updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        else:
            db.session.delete(new)
        db.session.commit()

    except Exception as e:
        print("error")
        print(str(e))
        return response.error(403, "Operation error.")

    return response.success()