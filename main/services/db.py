from flask import make_response, jsonify
from main.resources.message_templates import error_message
from bson.objectid import ObjectId


class DbOperations:
    def __init__(self, collections, schema):
        self.source_users = collections[0].user
        self.source_users_location = collections[0].user_location
        self.source_location = collections[0].location_lat
        self.source_bluetooth = collections[0].bluetooth_encounter

        self.collection_users = collections[1]
        self.schema = schema

    def insert(self, payload):
        "Inserting New User"

        payload = self.schema().load(payload)
        inserted_id = self.collection_users.insert(payload)
        return str(inserted_id)

    def find_all(self):
        "Querying all existing users"

        cursor = self.collection_users.find()
        result = self.schema(many=True).dumps(cursor)
        return make_response(result)

    def find_one(self, criteria):
        "Querying one target user"

        record = self.collection_users.find_one(criteria)
        results = self.schema().dump(record) if record is not None else error_message(criteria, 'No Record found')

        return make_response(results)

    def update(self, criteria, updated_value):
        "Updating one user information"
        if '_id' in list(criteria.keys()):
            criteria = {'_id': str(criteria['_id'])} # Changing ObjectId to regular string

        result = self.collection_users.replace_one(criteria, updated_value, upsert=True).modified_count

    def delete(self, criteria):
        "Deleting one user from database"

        result = self.collection_users.delete_one(criteria)
        return result.deleted_count

    def find_user_sources(self, criteria):
        "Querying user from source users"
        user = self.source_users.find_one(criteria)

        if user is not None:
            user.update({'_id': str(user['_id'])}) # Changing ObjectId to regular string
            user_json = self.schema().load(user)

            self.update(criteria, user_json) # Updating user data from source user tables
            self.find_bluetooth_data(criteria)
        else:
            return "No Match Found"

    def find_bluetooth_data(self, criteria):
        "Querying user data from source user bluetooth encounter table"
        user = self.source_bluetooth.find_one(criteria)

        if user is not None:
            user.update({
                '_id': str(user['_id']),
                'encounter_user_id': str(user['encounter_user_id']),
                }) # Changing ObjectId to regular string
            user_json = self.schema().load(user)

            self.update(criteria, user_json)
            self.find_location_data(criteria)
        else:

            self.find_location_data(criteria)


    def find_location_data(self, criteria):
        "Querying user location data from source database"
        user = self.source_users_location.find_one(criteria)

        if user is not None:
            user.update({
                '_id': str(user['_id']),
                'location_id': str(user['location_id'])
                }) # Changing ObjectId to regular string

            user_json = self.schema().load(user)
            self.update(criteria, user_json)

            criteria = {
                'location_id': ObjectId(user_json['location_id'])
            }
            self.find_target_location(criteria)
        else:
            return "No User Location Match"

    def find_target_location(self, criteria):
        "Querying Location Values from source database"
        user = self.source_location.find_one(criteria)
        
        if user is not None:
            user.update({'location_id': str(user['location_id'])}) # Changing ObjectId to regular string
            
            user_json = self.schema().dump(user)
            self.update(criteria, user_json)

        resp = jsonify("User Information Update Complete")
        resp.status_code = 200
        return resp
        