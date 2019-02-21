from model import User, Transfer
import mongoengine
mongoengine.connect("EASY_BANK")
import bcrypt
import jwt
import json
from datetime import datetime, timedelta
from keys import session_key

def signup(username,aadhar,DOB,password,address):
    try:
        hashedpass = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        user=User(aadhar=aadhar, username=username, password=hashedpass, DOB=datetime.strptime(DOB,"%d-%m-%Y"), address=address)
        user.save()
        token=jwt.encode({"user":user.username,"exp":datetime.now()+timedelta(hours=24)},session_key)
        return {"token":token.decode('utf-8'),"acc":user.accountNo}, 200
    except mongoengine.errors.NotUniqueError:
        return {"message":"UsernameAlreadyExists"}, 301
    except:
        return {"message":"WrongValues"}, 302


def transferMoney(token,recieverAcc,senderip,amount):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"message":"UnauthorizedRequest"}, 401
    else:
        try:
            cust = User.objects.get(username=tokenValidator[0])
            bankTransfer = Transfer(
                SenderAccount=cust.accountNo,
                ReceiverAccount=recieverAcc,
                Amount=amount,
                SenderIP=senderip
            )
            bankTransfer.save()
            return {"message":"AccountDoesnotExist"}, 200
        except mongoengine.errors.DoesNotExist:
            return {"message":"AccountDoesnotExist"}, 304
        except:
            return {"message":"Unknown message Occured"}, 501


def validateToken(token):
    try:
        username = jwt.decode(token, session_key)["user"]
        try:
            cust = User.objects.get(username=username)
            return cust.username, True
        except:
            return None, False
    except:
        return None, False
