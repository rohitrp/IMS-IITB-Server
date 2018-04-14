from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import json
from bson.json_util import loads, dumps

app = Flask(__name__)
api = Api(app)
client = MongoClient('localhost', 27017)
db = client['iitb_ims']

class Login(Resource):
    def get(self):
        data = request.args
        email = data['email']
        password = data['password']

        users = db.users

        user = users.find_one({'email': email})
        print(user)
        if user and user['password'] == password:
            return {'status': 1, 'email': user['email'], 'name': user['name']}
        else:
            return {'status': 0}

class Signup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('name', type=str)

    def post(self):
        data = self.parser.parse_args()

        print(data)
        users = db.users

        user = users.find_one({'email': data['email']})

        if user is None:
            user = users.insert_one(data)
            return {'status': 1, 'email': data['email']}
        else:
            return {'status': 0}

class CreatePaper(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('title', type=str)
    parser.add_argument('body', type=str)

    def post(self):
        data = self.parser.parse_args()

        papers = db.papers

        count = db.papers.count({'email': data['email']})
        data['id'] = count+1

        print(data)
        if papers.insert_one(data):
            return {'status': 1}
        else:
            return {'status': 0}

api.add_resource(Login, '/api/login/')
api.add_resource(Signup,'/api/signup/')
api.add_resource(CreatePaper, '/api/papers/create/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
