from flask import Flask,request,jsonify
from flask_restful import Resource,Api
from connectors import signup

app=Flask(__name__)
api=Api(app)


class Signup(Resource):
    def post(self):
        username=request.form.get("username")
        password=request.form.get("password")
        aadhar=request.form.get("aadhar")
        address=request.form.get("address")
        DOB=request.form.get("DOB")
        return jsonify(signup(username,aadhar,DOB,password,address))

api.add_resource(Signup,"/signup")

if __name__ == "__main__" :
    app.run(debug=True)               