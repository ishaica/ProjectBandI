from flask import Blueprint, render_template, request, flash, redirect, current_app 
from datetime import datetime
from db import db
from models import Host, Event
from form_validations.sign_up_validation import validate_host
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
     return render_template('admin_page.html', first_name='Ben', events=Event.query.all() ,hosts = Host.query.all())


@main.route('/admin_page/<int:id>', methods=['POST'])
def delete_event_by_id(id):
    event = Event.query.get(id)
    if not event:
        flash("Event not found")
        return render_template('admin_page.html', events=Event.query.all(), hosts=Host.query.all())
    db.session.delete(event)
    db.session.commit()
    flash(" Event deleted successfully ")
    return render_template('admin_page.html', events=Event.query.all(), hosts=Host.query.all())

@main.route('/pop_list')
def pop_list():
    return render_template('pop_list.html', events=Event.query.order_by(Event.event_date.desc(),
     Event.time.desc()).all())

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', input_email='')
    else:
        email = request.form['email']
        password = request.form['password']
        curr_host = Host.query.filter(Host.email.ilike(email.strip())).first()
        if curr_host:
            if curr_host.password.strip() == password.strip():
                return redirect(f'/host_page?name={curr_host.first_name}')
            else:
                flash("Incorrect Password")
                return render_template('login.html', input_email=email)
        else:
            flash("Incorrect Email and/or password, please try again")
            return render_template('login.html', input_email='')

@main.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        num_hosts = Host.query.count()
        return render_template('sign_up.html', form_data={}, errors={}, num_hosts=num_hosts)
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']   
        phone = request.form['phone']
        password1 = request.form['password1'].strip()
        password2 = request.form['password2'].strip()
        exists = Host.query.filter(Host.email.ilike(email.strip())).first()
        if exists:
            flash("already a member")
            return redirect('/')
    errors = validate_host(first_name, last_name, email, phone, password1, password2)
    if errors == {}:
        new_host = Host(first_name=first_name,last_name=last_name,
        email=email, phone=phone,password=password1)
        db.session.add(new_host)
        db.session.commit()
        return redirect('/after_sign_up')
    else:
        return render_template('sign_up.html', form_data=request.form, errors=errors)

@main.route('/after_sign_up', methods=['GET', 'POST'])
def after_sign_up():
    return render_template('after_sign_up.html')

@main.route('/index', methods=['GET', 'POST'])
def homepage_after():
    return render_template('home.html')

@main.route('/host_page', methods=['GET', 'POST'])
def host_page():
    name = request.args.get('name')
    return render_template('host_page.html', first_name=name)

@main.route('/new_event', methods=['GET', 'POST'])
def event_form():
    event_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    price_range = db.Column(db.String(30), nullable=False)
    if request.method == 'POST':
        event_type = request.form['event_type']
        description = request.form['description']
        address = request.form['address']
        event_date = datetime.strptime(request.form['event_date'], "%Y-%m-%d").date()
        time = datetime.strptime(request.form['time'], "%H:%M").time()
        price_range = request.form['price_range']
        exists = Event.query.filter(
            Event.address.ilike(address.strip()),
            Event.event_date == event_date,
            Event.time == time
        ).first()
        if exists:
            flash("Event already registered")
            return redirect('/my_events')
        message = validate_event(event_type, description, address, event_date, time, price_range)
        if message == "":
            new_event = Event(
                event_type=event_type,
                description=description,
                address=address,
                event_date=event_date,
                time=time,
                price_range=price_range,
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
