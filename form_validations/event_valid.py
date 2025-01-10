from flask import Flask, render_template, request
from datetime import datetime, timedelta
from form_validations.sign_up_validation import valid_word, valid_phone

def validate_event(event_type, description, address, event_date, time, price_range):
    res = ""
    if event_type == "select":
        res += "Event type" + "\n"
    if not description or len(description) > 100:
        res += "Description"+ "\n"
    if not address or len(address) > 100:
        res += "Address" + "\n"
    if not event_date or not (datetime.today().date() <= event_date <= (datetime.today().date() + timedelta(days=30))):
        res += "Date" + "\n"
    if not time:
        res += "Time" + "\n"
    if not price_range:
        res += "Price range" + "\n"
    return res + "not valid" if res != "" else ""