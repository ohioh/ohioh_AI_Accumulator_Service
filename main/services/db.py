from flask import make_response
from main.resources.message_templates import error_message


class DbOperations:
    def __init__(self, collections, schema):
        self.collections = collections
        self.schema = schema

    def insert(self, payload):
        payload = self.schema().load(payload)
        inserted_id = self.collections.insert_one(payload).inserted_id
        return str(inserted_id)

    def find_one(self, criteria):
        record = self.collections.find()
        results = self.schema(many=True).dump(record) if record is not None else error_message(criteria, 'No Record found')

        result = [user for user in results if user['_id'] == criteria['_id']]

        return make_response(result[0])

    def find_all(self):
        cursor = self.collections.find()
        result = self.schema(many=True).dumps(cursor)
        return make_response(result)

    def update(self, criteria, updated_value):
        result = self.collections.replace_one(criteria, updated_value, upsert=True).modified_count
        return result

    def delete(self, criteria):
        result = self.collections.delete_one(criteria)
        return result.deleted_count
