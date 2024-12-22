from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Time, Boolean
from db import db  

class Host (db.Model):
    __tablename__ = 'host'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    event_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False) 
    address = db.Column(db.String(100), nullable=False)
    event_date = db.Column(Date, nullable=False)
    time = db.Column(Time, nullable=False)
    price_range = db.Column(db.String(30), nullable=False)
    vegan_friendly = db.Column(Boolean, nullable=False, default=False)
    phone_number = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Host(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>"
