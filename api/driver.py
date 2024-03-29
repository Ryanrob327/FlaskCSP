from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.drivers import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/drivers')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate uid
            email = body.get('email')
            if email is None:
                return {'message': f'email is missing'}, 210
            # validate password
            password = body.get('password')
            if password is None:
                return {'message': f'password is missing'}, 210

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(name=name, 
                      email=email,
                      password=password)

            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or email {email} or password {password} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')