from flask import Blueprint, jsonify, render_template
from models import Host

api = Blueprint('api', __name__)

@api.route('/pop_list')
def pop_list():
    events = Host.query.order_by(Host.event_date.desc(), Host.time.desc()).all()
    return render_template('poplist.html', events=events)

@api.route('/events')
def get_events():
    events = Host.query.order_by(Host.event_date.desc(), Host.time.desc()).all()
    return jsonify([{
        "first_name": event.first_name,
        "last_name": event.last_name,
        "event_type": event.event_type,
        "description": event.description,
        "address": event.address,
        "event_date": event.event_date.isoformat(),
        "time": event.time.isoformat(),
        "price_range": event.price_range,
        "vegan_friendly": event.vegan_friendly,
        "phone_number": event.phone_number
    } for event in events])

