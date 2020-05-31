import json
from flask import request
from main import mongo, mongo1, mongo2, mongo3, mongo4
from flask_restful import Resource
from ..schemas.users import UserSchema
from ..services.db import DbOperations

from bson.objectid import ObjectId


users = mongo.ohioh

cluster1 = mongo1.ohioh
cluster2 = mongo2.ohioh
cluster3 = mongo3.ohioh
cluster4 = mongo4.ohioh


db = DbOperations(
    collections=[
        users,
        cluster1,
        cluster2,
        cluster3,
        cluster4
    ],
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

    def put(self, user_id):

        try:
            criteria={
                '_id': ObjectId(user_id)
            }
            return db.find_user_sources(criteria)

        except Exception as e:
            return "Error - %s" % e


    def delete(self, user_id):
        return db.delete(
            criteria={'_id': user_id}
        )
