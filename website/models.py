from ast import Try
from enum import unique
from . import db
from flask_login import UserMixin

class Locomotive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series = db.Column(db.String(150), nullable=False)
    number = db.Column(db.String(150), nullable=False)
    power_type = db.Column(db.String(150), nullable=False)
    factory = db.Column(db.String(150), nullable=False)
    number_of_sections = db.Column(db.String(150), nullable=False)
    construction_speed = db.Column(db.String(150), nullable=False)
    type_of_braking = db.Column(db.String(150), nullable=False)
    opisanie = db.Column(db.String(150), nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Nov(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)

    