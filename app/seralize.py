from flask import Flask
from extensions.extensions import ma,db
from app.model import User,Todo
from marshmallow import validate,fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    name =fields.String(required=True,validate=[validate.Length(min=2,max=20)])
    surname =fields.String(required=True,validate=[validate.Length(min=2,max=20)])
    nickname =fields.String(required=True,validate=[validate.Length(min=2,max=20)])
    password =fields.String(required=True,validate=[validate.Length(min=8,max=40)])
    email=fields.Email(required=True)

    class Meta(ma.Schema):
        model = User
        load_instance=True
        
class UpdateUserSchema(ma.Schema):
    name=fields.String()
    nickname=fields.String()
    surname=fields.String()
    email=fields.Email()
    password=fields.String()

class TodoSchema(ma.SQLAlchemyAutoSchema):
    date = fields.DateTime("%Y-%m-%d",required=True)
    remindime = fields.DateTime("%Y-%m-%d",required=True)

    class Meta(ma.Schema):
        model = Todo
        load_instance=True

class UpdateTodoSchema(ma.Schema):
    date = fields.DateTime("%Y-%m-%d")
    remindime = fields.DateTime("%Y-%m-%d")