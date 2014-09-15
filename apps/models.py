"""
models.py

"""
from apps import db


class Rda(db.Model):
    seq = db.Column(db.Integer, primary_key=True)
    kcal = db.Column(db.Integer)
    na = db.Column(db.Integer)
    sugar = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    sater_fat = db.Column(db.Integer)

class Food(db.Model):
    seq = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(255))
    description = db.Column(db.Text())
    food_amount = db.Column(db.Integer)
    food_cal = db.Column(db.Integer)
    food_na = db.Column(db.Integer)
    food_sugar = db.Column(db.Integer)
    food_fat = db.Column(db.Integer)
    food_satur = db.Column(db.Integer)
    food_protein = db.Column(db.Integer)

class User(db.Model):
    seq = db.Column(db.Integer, primary_key=True)
    rda_seq = db.Column(db.Integer, db.ForeignKey('rda.seq'))
    rda = db.relationship('Rda',backref=db.backref('rdaconnect', cascade='all, delete-orphan', lazy='dynamic'))
    user_id = db.Column(db.String(255))
    user_pw = db.Column(db.String(255))
    user_name = db.Column(db.String(255))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    regdate = db.Column(db.DateTime(), default=db.func.now())

class Food_reg(db.Model):
    seq = db.Column(db.Integer, primary_key=True)
    user_seq = db.Column(db.Integer, db.ForeignKey('user.seq'))
    user = db.relationship('User',backref=db.backref('uconnect', cascade='all, delete-orphan', lazy='dynamic'))
    food_seq = db.Column(db.Integer, db.ForeignKey('food.seq'))
    food = db.relationship('Food', backref=db.backref('foodconnect', cascade='all, delete-orphan', lazy='dynamic'))
    eat_date = db.Column(db.DateTime())
    eat_type = db.Column(db.Integer)
    photo = db.Column(db.String(255))
    count = db.Column(db.Integer)
    description = db.Column(db.Text())
    regdate = db.Column(db.DateTime(), default=db.func.now())

class resultAn(db.Model):
    seq = db.Column(db.Integer, primary_key=True)
    user_seq = db.Column(db.Integer, db.ForeignKey('user.seq'))
    user = db.relationship('User', backref=db.backref('userconnect', cascade='all, delete-orphan', lazy='dynamic'))
    result = db.Column(db.Integer)
    regdate = db.Column(db.DateTime(), default=db.func.now())