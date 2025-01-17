from flask import Blueprint, render_template, request, flash, redirect, current_app 
from datetime import datetime , timedelta
from db import db
from models import Event
from form_validations.event_valid import validate_event

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('home.html')

@main.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin_login.html', input_username = '')
    else:
        username = request.form['username']
        password = request.form['password']
        if username == current_app.config['ADMIN_USERNAME'] and password == current_app.config['ADMIN_PASSWORD']:
            return redirect('/admin_page')
        else:
            flash("Incorrect Username and/or Password, please try again")
            return render_template('admin_login.html', inpute_username=username)

@main.route('/admin_page', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'GET':
     return render_template('admin_page.html', first_name='Ben', events=Event.query.all())


@main.route('/admin_page/<int:id>', methods=['POST'])
def delete_event_by_id(id):
    event = Event.query.get(id)
    if not event:
        flash("Event not found")
        return render_template('admin_page.html', events=Event.query.all())
    db.session.delete(event)
    db.session.commit()
    flash(" Event deleted successfully ")
    return render_template('admin_page.html', events=Event.query.all())

@main.route('/pop_list')
def pop_list():
    date_a = datetime.now().date()
    date_b = (datetime.now() + timedelta(days=7)).date()
    event_count = Event.query.filter(Event.event_date >= date_a, Event.event_date <= date_b).count()
    return render_template('pop_list.html', event_count=event_count)
    
@main.route('/food_list')
def food_list():
    return render_template('food_list.html')

@main.route('/drink_list')
def music_list():
    return render_template('drink_list.html')

@main.route('/art_list')
def art_list():
    return render_template('art_list.html')

@main.route('/index', methods=['GET', 'POST'])
def homepage_after():
    return render_template('home.html')


@main.route('/new_event', methods=['GET', 'POST'])
def event_form():
    host = db.Column(db.String(30), nullable=False)
    event_name = db.Column(db.String(20), nullable=False)
    event_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    price_range = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    if request.method == 'POST':
        host = request.form['host']
        event_name = request.form['event_name']
        event_type = request.form['event_type']
        description = request.form['description']
        address = request.form['address']
        event_date = datetime.strptime(request.form['event_date'], "%Y-%m-%d").date()
        time = datetime.strptime(request.form['time'], "%H:%M").time()
        price_range = request.form['price_range']
        phone = request.form['phone']
        exists = Event.query.filter(
            Event.address.ilike(address.strip()),
            Event.event_date == event_date,
            Event.time == time
        ).first()
        if exists:
            flash("Event already registered")
            return redirect('/my_events')
        message = validate_event(host,event_name,event_type, description, address, event_date, time, price_range, phone)
        if message == "":
            new_event = Event(
                host=host,
                event_name=event_name,
                event_type=event_type,
                description=description,
                address=address,
                event_date=event_date,
                time=time,
                price_range=price_range,
                phone=phone
            )
            db.session.add(new_event)
            db.session.commit()
            return render_template('my_events.html', my_events=Event.query.all())
        else:
            flash(message)
            return render_template('new_event.html', form_data=request.form)
    return render_template('new_event.html')

@main.route('/my_events')
def my_events():
    my_events = Event.query.order_by(Event.event_date.desc(), Event.time.desc()).all()
    return render_template('my_events.html', my_events=my_events)

@main.route('/delete_my_event_by_id/<int:id>', methods=['POST'])
def delete_my_event_by_id(id):
    event = Event.query.get(id)
    if not event:
        flash("Event not found")
        return render_template('my_events.html')
    db.session.delete(event)
    db.session.commit()
    flash("Event deleted successfully")
    return render_template('my_events.html', my_events=Event.query.all())
