from flask import Flask, render_template, request
from datetime import datetime, timedelta

def valid_phone(phone):
    errors = []
    if phone[:2]!="05":
        errors.append("Phone number must start with 05")
    l = len(phone)
    if l!=10:
        if l == 13 and phone[3:5] != " - " or l == 11 and phone[3] != "-":
            errors.append("Phone number must have 10 digits")
        elif l>13 or l<10:
            errors.append("Phone number must have 10 digits")
    return errors

def valid_word(word):
    errors = []
    if word[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        errors.append("Capital letter")
    for char in word[1:]:
        if char not in "abcdefghijklmnopqrstuvwxyz":
            errors.append("only letters")
    return errors

def validate_event(host, event_name, event_type, description, address, event_date, time, price_range, phone):
    res = ""
    for word in (host + "" + event_name):
        if valid_word(word):
            res += "Event name" if word in event_name else "Host Name" + "\n"
            break
    if valid_word(host):
        res += "Host" + "\n"
    if valid_word(event_name):
        res += "Event name" + "\n"
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
    if valid_phone(phone):
        res += "Phone number" + "\n"
    return res + "not valid" if res != "" else ""