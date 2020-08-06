from flask import Flask
from werkzeug.security import check_password_hash ,generate_password_hash
from extensions.extensions import db,ma
from datetime import datetime

class User(db.Model):
    __tablename__="User"
    id = db.Column(db.Integer(),primary_key= True)
    name = db.Column(db.String(),nullable=False)
    surname = db.Column(db.String(),nullable=False)
    nickname = db.Column(db.String(),nullable=False)
    email = db.Column(db.String(),unique=True,nullable=False)
    password = db.Column(db.String(),nullable=False)
    todo = db.relationship('Todo')

    def set_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def savedb(self):
        db.session.add(self)
        db.session.commit()
    def deletedb(self):
        db.session.delete(self)
        db.session.commit()
    def update(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)
        self.savedb()


class Todo(db.Model):
    __tablename__= "Todo"
    id = db.Column(db.Integer(),primary_key=True)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    remindime = db.Column(db.DateTime,nullable=False)
    user_id = db.Column(db.Integer(),db.ForeignKey("User.id"),nullable=False)

    def savedb(self):
        db.session.add(self)
        db.session.commit()
    def deletedb(self):
        db.session.delete(self)
        db.session.commit()
    def update(self,**kwargs):
        for key ,value in kwargs.items():
            setattr(self,key,value)
        self.savedb()