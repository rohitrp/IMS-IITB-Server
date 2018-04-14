from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient

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
        if user and user.password == password:
            return "SUCCESS"
        else:
            return "FAILED"

api.add_resource(Login, '/api/login/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
