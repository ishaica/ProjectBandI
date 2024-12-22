from flask import Blueprint, render_template, request, flash
from datetime import datetime
from db import db
from models import Host
from form_validation import validate_input

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    return render_template('home.html')

@main.route('/host_form', methods=['GET', 'POST'])
def host_form():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        event_type = request.form['event_type']
        description = request.form['description']
        address = request.form['address']
        event_date = datetime.strptime(request.form['event_date'], "%Y-%m-%d").date()
        time = datetime.strptime(request.form['time'], "%H:%M").time()
        price_range = request.form['price_range']
        vegan_friendly = request.form.get('vegan_friendly', 0)
        phone_number = request.form['phone_number']

        exists = Host.query.filter(
            Host.first_name.ilike(first_name.strip()),
            Host.last_name.ilike(last_name.strip()),
            Host.event_date == event_date,
            Host.time == time
        ).first()

        if exists:
            flash("Application in process")
            return render_template('form.html', form_data=request.form)

        message = validate_input(first_name, last_name, event_type, description, address, event_date, time, price_range, phone_number)
        if message == "":
            new_host = Host(
                first_name=first_name,
                last_name=last_name,
                event_type=event_type,
                description=description,
                address=address,
                event_date=event_date,
                time=time,
                price_range=price_range,
                vegan_friendly=int(vegan_friendly),
                phone_number=phone_number
            )
            db.session.add(new_host)
            db.session.commit()
            return render_template('sent.html')
        else:
            flash(message + " not valid")
            return render_template('form.html', form_data=request.form)
    return render_template('form.html')

@main.route('/pop_list')
def pop_list():
    events = Host.query.order_by(Host.event_date.desc(), Host.time.desc()).all()
    return render_template('poplist.html', events=events)
