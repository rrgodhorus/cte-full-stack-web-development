from model import User
import mongoengine
mongoengine.connect("EASY_BANK")
import bcrypt
import jwt
from datetime import datetime, timedelta
from keys import session_key

def signup(username,aadhar,DOB,password,address):
    try:
        hashedpass = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        user=User(aadhar=aadhar, username=username, password=hashedpass, DOB=datetime.strptime(DOB,"%d-%m-%Y"), address=address)
        user.save()
        token=jwt.encode({"user":user.username,"exp":datetime.now()+timedelta(hours=24)},session_key)
        return {"token":token.decode('utf-8')}
    except mongoengine.errors.NotUniqueError:
        return{"error":"UsernameAlreadyExists","message":301}
    except:
        return{"error":"WrongValues","message":302}