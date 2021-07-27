from flask import Flask, jsonify,request
from flask_restful import Api,Resource
from pymongo import MongoClient
import bcrypt
import requests
import subprocess
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')

db = client.ImageRecognition
users = db["Users"]

def UserExist(username):
    if users.find({"username":username}).count()==0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData['username']
        password = postedData['password']

        if UserExist(username):
            resJson = {
                "status":301,
                "msg":"Invalid username"
            }
            return jsonify(resJson)

        hashed_password = bcrypt.hashpw(password.encode("utf8"),bcrypt.gensalt())

        users.insert({
            "username":username,
            "password":hashed_password,
            "tokens":5
        })

        resJson = {
            "status":201,
            "msg":"You successfully signed up for this Api."
        }

        return jsonify(resJson)

def verify_password(username,password):
    if not UserExist(username):
        return False
    
    hashed_pw = users.find({
        "username":username
    })[0]["password"]

    if bcrypt.hashpw(password.encode("utf8"),hashed_pw) == hashed_pw:
        return True
    else:
        return False


def get_response(status,msg):
    resJson = {
        "status":status,
        "msg":msg
    }
    return resJson

def verify_credentials(username,password):
    if not UserExist(username):
        return get_response(301,"Invalid username"),True
    
    correct_pw = verify_password(username,password)
    if not correct_pw:
        return get_response(301,"Invalid password"),True
    
    return None,False

class Classify(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        url = postedData["url"]

        resJson,error = verify_credentials(username,password)

        if error:
            return jsonify(resJson)

        tokens = users.find({
            "username":username
        })[0]["tokens"]

        if tokens<=0:
            return jsonify(get_response(303,"Not enough tokens"))

        r = requests.get(url)
        resJson = {}
        with open("temp.jpg","wb") as f:
            f.write(r.content)
            proc = subprocess.Popen("python classify_image.py --model_dir=. --image_file=./temp.jpg")
            proc.communicate()[0]
            proc.wait()
            with open("text.txt") as g:
                resJson = json.load(g)
            
            users.update({
                "username":username
            },{
                "$set":{
                    "tokens":tokens-1
                }
            })

            return resJson


class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        amount = postedData["amount"]

        if not UserExist(username):
            return jsonify(get_response(301,"Invalid username"))

        correct_pw = "abc123"
            
        if not password==correct_pw:
            return jsonify(get_response(302,"Invalid Administrator Password"))

        users.update({
            "username":username
        },{
            "$set":{
                "tokens":amount
            }
        })

        return jsonify(get_response(200,"Refilled Successfully!"))


api.add_resource(Register,'/register')
api.add_resource(Classify,'/classify')
api.add_resource(Refill,'/refill')

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)