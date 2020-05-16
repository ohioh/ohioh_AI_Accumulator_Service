from flask import Blueprint
from .users import UserList, User
from flask_restful import Api

from .beat import Beat

api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix='/ohioh/accumulator/api/v1')

api.add_resource(Beat, '/')
api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<user_id>')


# api.add_resource()
