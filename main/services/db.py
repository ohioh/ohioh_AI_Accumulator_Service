from flask import make_response, jsonify
from main.resources.message_templates import error_message
from bson.objectid import ObjectId
import requests


class DbOperations:
    def __init__(self, collections, schema):
        self.collection_users = collections.users
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
        results = self.schema().dump(record) if record is not None else error_message(criteria, 'No record found!')

        return make_response(results)

    def update(self, criteria, update):
        "Updating one user information"
        new_value = { "$set": update }
        result = self.collection_users.update_one(criteria, new_value, upsert=True).modified_count
        return result

    def delete(self, criteria):
        "Deleting one user from database"

        result = self.collection_users.delete_one(criteria)
        return result.deleted_count



    def find_user_sources(self, criteria):
        "Querying user from source users"
        user_id = criteria['_id']

        user = requests.get(f"http://49.12.77.250:3400/ohioh/api/v1/users/{user_id}")
        data = user.json()

        try:
            result = data['message']

        except KeyError:
            import pdb; pdb.set_trace()
            user_json = self.schema().dump(data)

            self.update(criteria, user_json)

            result = self.find_bluetooth_data(criteria)
        
        return result

    def find_bluetooth_data(self, criteria):
        "Querying user data from source user bluetooth encounter table"
        user_id = criteria['_id']

        user = requests.get(f"http://49.12.104.168:3400/ohioh/api/v1/bluetooth-encounter/{user_id}")
        data = user.json()

        try:
            result = data['message']

        except KeyError:
            user_json = self.schema().dump(data)

            self.update(criteria, user_json)
        
        self.find_user_location_data(criteria)


    def find_user_location_data(self, criteria):
        "Querying user location data from source database"
        user_id = criteria['_id']

        user = requests.get(f"http://49.12.73.42:3400/ohioh/api/v1/user-location/{user_id}")
        data = user.json()

        try:
            return "User data accumulated completely, but no location data found!"

        except KeyError:
            user_json = self.schema().dump(data)

            self.update(criteria, user_json)

            #Add location_id as criteria to search for location data
            criteria = {"location_id": data['location_id']}

            self.find_location_data(criteria)

    def find_location_data(self, criteria):
        "Querying all the location data attached to this user"
        location_id = criteria['location_id']

        user = request.get(f"http://49.12.104.245:3400/ohioh/api/v1/location-lat/{location_id}")
        data = user.json()

        user_json = self.schema().dump(data)
                
        self.update(criteria, user_json)

        return "User data accumulated completely"

        