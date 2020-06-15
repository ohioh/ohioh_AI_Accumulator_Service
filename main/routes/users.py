import json
from flask import request
from main import mongo
from flask_restful import Resource
from ..schemas.users import UserSchema
from ..services.db import DbOperations
from bson.objectid import ObjectId


users = mongo.ohioh


db = DbOperations(
    collections=users,
    schema=UserSchema
    )


class UserList(Resource):
    def get(self):
        return db.find_all()

    def post(self):
        payload = request.get_json()
        return db.insert(payload)


class User(Resource):
    def get(self, user_id):
        return db.find_one(
            criteria={'_id': user_id}
        )

    def post(self, user_id):
        criteria={
            '_id': user_id
        }
        return db.find_user_sources(criteria)        

    def put(self, user_id):

        try:
            payload = request.get_json()
            return db.update(
                criteria = {'_id': user_id},
                update = payload
            )

        except Exception:
            return "User not found!"


    def delete(self, user_id):
        return db.delete(
            criteria={'_id': user_id}
        )
