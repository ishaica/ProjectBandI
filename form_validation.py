from flask import Flask, render_template, request
from datetime import datetime, timedelta

def valid_word(word):
    if word[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return False
    for char in word[1:]:
        if char not in "abcdefghijklmnopqrstuvwxyz":
            return False
    return True
def valid_phone(phone):
    if phone[:2]!="05" and len(phone)!=10:
        return False
    return True
def validate_input(first_name, last_name, event_type, description, address, event_date, time, price_range, phone_number):
    res = ""
    if len(first_name) > 20 or not valid_word(first_name):
        res += "First name, "
    if len(last_name) > 30 or not valid_word(last_name):
        res += "Last name, "
    if event_type == "select":
        res += "Event type, "
    if not description or len(description) > 100:
        res += "Description, "
    if not address or len(address) > 100:
        res += "Address, "
    event_date_obj = datetime.strptime(event_date, "%Y-%m-%d").date()
    if not event_date or not (datetime.today().date() <= event_date_obj <= (datetime.today().date() + timedelta(days=30))):
        res += "Date, "
    if not time:
        res += "Time,"
    if not price_range:
        res += "Price range, "
    if not valid_phone(phone_number):
        res += "Phone number, "
    return res + " input not valid" if res!="" else res