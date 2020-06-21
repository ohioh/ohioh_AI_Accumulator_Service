from flask import make_response, jsonify
from main.resources.message_templates import error_message
from bson.objectid import ObjectId
import requests
from jsonmerge import merge

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
        self.collection_users.update_one(criteria, new_value, upsert=True)

    def delete(self, criteria):
        "Deleting one user from database"

        result = self.collection_users.delete_one(criteria)
        return result.deleted_count


    def find_user_sources(self, criteria):
        "Querying user from source users"
        user_id = criteria['_id']

        # Extract from Clusters
        user_data = self.find_user_data(user_id)
        bluetooth_data = self.find_bluetooth_data(user_id)
        user_location_data = self.find_user_location_data(user_id)
        location_data = self.find_location_data(user_id)

        #merging
        result1 = merge(user_data, bluetooth_data)
        result2 = merge(result1, user_location_data)

        result = merge(result2, location_data)

        try:
            return user_data['message']

        except KeyError:
            # import pdb; pdb.set_trace()
            user_json = self.schema().load(result)

            self.update(criteria, user_json)

            return "User data uploaded to Accumulator successfully!"

    def find_user_data(self, user_id):
        "Querying all user data from Cluster 1"
        user = requests.get(f"http://49.12.77.250:3400/ohioh/api/v1/users/{user_id}")
        data = user.json()

        return data

    def find_bluetooth_data(self, user_id):
        "Querying all user data from Cluster 2"
        user = requests.get(f"http://49.12.104.168:3400/ohioh/api/v1/bluetooth-encounter/{user_id}")
        data = user.json()

        # Renaming data time fields
        data['bluetooth_timestamp'] = data['user_timestamp']
        del data['user_timestamp']

        return data

    def find_user_location_data(self, user_id):
        "Querying all user data from Cluster 2"
        user = requests.get(f"http://49.12.73.42:3400/ohioh/api/v1/user-location/{user_id}")
        data = user.json()

        data['user_location_timestamp'] = data['user_timestamp']
        del data['user_timestamp']

        return data

    def find_location_data(self, user_id):
        "Querying all the location data attached to this user"

        user = requests.get(f"http://49.12.104.245:3400/ohioh/api/v1/location-lat/{user_id}")
        data = user.json()

        data['location_timestamp'] = data['user_timestamp']
        del data['user_timestamp']

        return data

        