from flask import Blueprint, jsonify, render_template
from models import Event

api = Blueprint('api', __name__)

@api.route('/events')   
def get_events():
    events = Event.query.order_by(Event.event_date.desc(), Event.time.desc()).all()
    return jsonify([{
        "event_type": event.event_type,
        "description": event.description,
        "address": event.address,
        "event_date": event.event_date.isoformat(),
        "time": event.time.isoformat(),
        "price_range": event.price_range,
    } for event in events])

