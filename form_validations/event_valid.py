from flask import Flask, render_template, request
from datetime import datetime, timedelta
from form_validations.general import valid_word, valid_phone

def validate_input(event_type, description, address, event_date, time, price_range):
    res = ""
    if event_type == "select":
        res += "Event type" + "\n"
    if not description or len(description) > 100:
        res += "Description"+ "\n"
    if not address or len(address) > 100:
        res += "Address" + "\n"
    event_date_obj = datetime.strptime(event_date, "%Y-%m-%d").date()
    if not event_date or not (datetime.today().date() <= event_date_obj <= (datetime.today().date() + timedelta(days=30))):
        res += "Date" + "\n"
    if not time:
        res += "Time" + "\n"
    if not price_range:
        res += "Price range" + "\n"
    return ",".join(res) if res != "" else ""