from flask import Flask,request,jsonify, make_response
from flask_restful import Resource,Api
from connectors import signup, transferMoney

app=Flask(__name__)
api=Api(app)


class Signup(Resource):
    def post(self):
        username=request.form.get("username")
        password=request.form.get("password")
        aadhar=request.form.get("aadhar")
        address=request.form.get("address")
        DOB=request.form.get("DOB")
        signerup = signup(username,aadhar,DOB,password,address)
        return make_response(jsonify(signerup[0]),signerup[1])

class TransferMoney(Resource):
    def post(self):
        token=request.headers.get("token")
        receiverAcc=request.form.get("receiverAcc")
        ipAddr=request.form.get("ipAddr")
        amount=request.form.get("amount")
        moneyTransferMech = transferMoney(token,receiverAcc,ipAddr,amount)
        return make_response(jsonify(moneyTransferMech[0]),moneyTransferMech[1])



api.add_resource(Signup,"/signup")
api.add_resource(TransferMoney, '/transfermoney')

if __name__ == "__main__" :
    app.run(debug=True)               