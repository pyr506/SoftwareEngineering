from flask import jsonify, request, g, url_for, current_app
from . import api, response
from .. import app, db
from app.models.event import Event
from app.models.user import User
from .decorators import token_required
from datetime import datetime

@api.route('/events', methods = ['GET'])
def get_events():
    events = Event.query.all()
    data = []
    for event in events:
        data.append(event.to_json())
    return response.success(data)

@api.route('/events/<int:events_id>', methods = ['GET'])
def get_event(events_id):
    event = Event.query.get(events_id)
    if not event:
        return response.error(404, "Event not found")
    event.clicked = event.clicked + 1
    db.session.commit()

    return response.success(event.to_json())


@api.route('/events', methods = ['POST'])
@token_required
def create_event(f):
    title = request.json.get('title')
    content = request.json.get('content')
    if not title:
        return response.error(403, "Missing Title parameter")
    if not content:
        return response.error(403, "Missing Content parameter")
    try:
        event = Event(title=title, content=content, user_id=f.id, location=request.remote_addr)
        db.session.add(event)
        db.session.commit()
        return response.success()
    except Exception as err:
        print(str(err))
        if "Duplicate entry" in str(err):
            return response.error(403, "'%s' Already Exist." % name)
        else:
            return response.error(403, "Operation error.")
    

@api.route('/events/<int:events_id>', methods = ['PUT', 'PATCH', 'DELETE'])
@token_required
def update_event(f, events_id):
    try:
        if not events_id:
            return response.error(403, "Missing events_id parameter")

        event = Event.query.filter_by(id=events_id).first()

        if not event:
            return response.error(403, "Event not found")

        if request.method in ['PUT','PATCH']:
            title = request.json.get('title')
            content = request.json.get('content')
            if not title:
                return response.error(403, "Missing Title parameter")
            if not content:
                return response.error(403, "Missing Content parameter")
            event.title = title
            event.content = content
            event.location = request.remote_addr
            event.updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        else:
            db.session.delete(event)
        db.session.commit()

    except Exception as e:
        print("error")
        print(str(e))
        return response.error(403, "Operation error.")

    return response.success()