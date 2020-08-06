from flask import Flask, request, jsonify
from app_init.app_factory import createAp
from flask import jsonify, current_app, request
from flask import Flask, jsonify, request
from http import HTTPStatus
import os
from werkzeug.security import generate_password_hash
import warnings
from app.seralize import TodoSchema,UserSchema,UpdateUserSchema,UpdateTodoSchema
from app.model import User,Todo
from http import HTTPStatus
from marshmallow import ValidationError
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,create_refresh_token,jwt_refresh_token_required,
    get_jwt_identity
)

warnings.simplefilter("ignore")
settings_name = os.getenv("settings")
app = createAp(settings_name)


@app.route("/user/login",methods=["POST"])
def Login():
    if not request.get_json():
        return jsonify(msg="error"),HTTPStatus.BAD_REQUEST
    email = request.json.get("email")
    password = request.json.get("password")
    if not email:
        return jsonify(msg="Wrong Email"),HTTPStatus.BAD_REQUEST
    if not password:
        return jsonify(msg="Wrong Password"),HTTPStatus.BAD_REQUEST
    user = User.query.filter_by(email=email).first()
    if user:
        if user.check_password(password):
            # access_token = create_access_token(identity=user.id)
            token = {
                    'access_token': create_access_token(identity=user.id),
                    'refresh_token': create_refresh_token(identity=user.id)
                }
            return jsonify(token),HTTPStatus.OK
        return jsonify(msg="User not founded"),HTTPStatus.NOT_FOUND

@app.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    user = get_jwt_identity()
    print(user)
    if user:
        access_token= create_access_token(identity=user)
        return jsonify({"Access Token:":access_token}),HTTPStatus.OK
    return jsonify(msg="ERROR"),HTTPStatus.NOT_FOUND

@app.route("/user",methods=["POST"])
def createUser():
    data = request.get_json()
    try:
        x = UserSchema().load(data)
        x.set_password()
        x.savedb()
    except ValidationError as err:
        return jsonify(err.messages),HTTPStatus.BAD_REQUEST
    return UserSchema().jsonify(x),HTTPStatus.OK


@app.route("/user",methods=["GET"])
@jwt_required
def UserGet():
    identity = get_jwt_identity()
    data = User.query.filter_by(id=identity).first()
    if data:
        return UserSchema().jsonify(data),HTTPStatus.OK
    return jsonify(msg="error"),HTTPStatus.BAD_REQUEST

@app.route("/user",methods=["GET"])
def UserAllGet():
    dataall=User.query.all()
    return UserSchema().jsonify(dataall,many=True),HTTPStatus.OK
    
@app.route("/user",methods=["PUT"])
@jwt_required
def UpdateUser():
    identity=get_jwt_identity()
    data = User.query.filter_by(id=identity).first()
    if data:
        user = request.get_json()
        data1 = UpdateUserSchema().load(user)
        data.update(**data1)
        return UserSchema().jsonify(data1),HTTPStatus.OK
    return jsonify(msg="error"),HTTPStatus.NOT_FOUND

@app.route("/user",methods=["DELETE"])
@jwt_required
def DeleteUserMethod():
    identity=get_jwt_identity()
    data = User.query.filter_by(id=identity).first()
    if data:
        data.deletedb()
        return jsonify(msg="Silinmisdir"),HTTPStatus.OK
    return jsonify(msg="error")


@app.route("/user/todo",methods=["POST"])
@jwt_required
def CreateUserTodo():
    identity=get_jwt_identity()
    data = request.get_json()
    if data:
        try:
            user = User.query.get(identity)
            if user:
                create=TodoSchema().load(data)
                create.user_id=user.id
                create.savedb()
        except ValidationError as err:
            return jsonify(err.messages),HTTPStatus.BAD_REQUEST
        return TodoSchema().jsonify(create),HTTPStatus.OK



@app.route("/user/<int:id>/todo",methods=["GET"])
@jwt_required
def GetUserTodoMethods(id):
    identity=get_jwt_identity()
    data = Todo.query.filter_by(user_id=identity,id=id).first()
    if data:
        return TodoSchema().jsonify(data),HTTPStatus.OK
    return jsonify(msg="Error"),HTTPStatus.BAD_REQUEST

@app.route("/user/todo", methods=["GET"])
@jwt_required
def GetUserTodoAllMethods():
    identity= get_jwt_identity()
    dataAll = Todo.query.filter_by(user_id=identity).all()
    return TodoSchema().jsonify(dataAll, many=True), HTTPStatus.OK

@app.route("/user/<int:id>/todo",methods=["PUT"])
@jwt_required
def TodoUpdateMethods(id):
    identity=get_jwt_identity()
    dataUpdate = Todo.query.filter_by(user_id=identity,id=id).first()
    if dataUpdate:
        data = request.get_json()
        data1 = UpdateTodoSchema().load(data)
        dataUpdate.update(**data1)
        return UpdateTodoSchema().jsonify(data1),HTTPStatus.OK
    return jsonify(msg= "Sehvdir"),HTTPStatus.BAD_REQUEST


@app.route("/user/<int:id>/todo",methods=["DELETE"])
@jwt_required
def DeleteProductsMethodss():
    identity=get_jwt_identity()
    data = Todo.query.filter_by(user_id = identity,id=id).first()
    if data:
        data.deletedb()
        return jsonify(msg=True),HTTPStatus.OK
    return jsonify(msg="errorrr"),HTTPStatus.BAD_REQUEST
