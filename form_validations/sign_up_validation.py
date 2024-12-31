from flask import Flask, render_template, request

def valid_word(word):
    errors = []
    if word[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        errors.append("Capital letter")
    for char in word[1:]:
        if char not in "abcdefghijklmnopqrstuvwxyz":
            errors.append("only letters")
    return errors

def valid_phone(phone):
    errors = []
    if phone[:2]!="05":
        errors.append("Phone number must start with 05")
    if len(phone)!=10:
        errors.append("Phone number must have 10 digits")
    return errors

def valid_email_suffix(email):
    main_suffix_options = [".com", ".org", ".net", ".edu", ".gov"]
    if email[-4:] not in main_suffix_options and email[-6:]!=".co.il":
        return False
    return True
def valid_email(email):
    errors = []
    if "@" not in email or not valid_email_suffix(email):
        errors.append("Email not valid")
    return errors
    
def valid_password(password):
    errors = []
    if len(password)<8:
        errors.append("Password must be at least 8 characters")
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain a number")
    if not any(c.isupper() for c in password):
        errors.append("Password must contain an uppercase letter")
    return errors

def validate_input(first_name, last_name, email, phone, password1, password2):
    
    output = {"First Name": [], "Last Name": [], "Email": [], "Phone": [], "Password": []}
    
    curr = valid_word(first_name)
    if len(first_name) > 20:
        output["First Name"].append("First name must be less than 20 characters") 
    if curr:
        output["First Name"] += curr
    
    curr = valid_word(last_name)
    if len(last_name) > 30:
        output["Last Name"].append("Last name must be less than 30 characters")
    if curr:
        output["Last Name"] += curr
    
    curr = valid_email(email)
    if len(email) > 50:
        output["Email"].append("Email must be less than 50 characters")
    if curr:
        output["Email"] += curr

    curr = valid_phone(phone)
    if curr:
        output["Phone"] += curr
    
    curr = valid_password(password1)
    if curr:
        output["Password"] += curr

    if password1 != password2:
        output["Password"].append("Passwords don't match")
    
    del_key = []
    for key in output:
        if output[key] == []:
            del_key.append(key)
    for key in del_key:
        del output[key]

    return output