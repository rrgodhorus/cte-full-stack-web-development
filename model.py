from mongoengine import Document, StringField, BinaryField, BooleanField, DateField, IntField, DecimalField, DateTimeField
import bcrypt
import datetime
import mongoengine
class User(Document):
    username=StringField(max_length=25,minimum_length=8,required=True)
    password=BinaryField(required=True)
    DOB = DateField(required = True)
    firstTimeUser=BooleanField(required=True,default=True)
    aadhar = IntField(required=True)
    address = StringField()
    accountNo = IntField(required=True, unique=True)
    balance = DecimalField(required=True, min_value=1000, default=5000)
    
    def save(self, *args, **kwargs):
        if (len(str(self.aadhar)) != 12):
            raise Exception("InvalidAadhar")
        if not self.accountNo:
            fobj = open('lastnum','r')
            lastAcc = int(fobj.read())
            fobj.close()
            self.accountNo = lastAcc+1
            fobj = open('lastnum','w')
            fobj.write(str(self.accountNo))
            fobj.close()
        super().save(self, *args, **kwargs)

class Transfer(Document):
    SenderAccount = IntField(required = True)
    ReceiverAccount = IntField(required = True)
    Amount = DecimalField(required = True, min_value=0)
    SenderIP = StringField(max_length=15,min_length=8)
    Date = DateTimeField(required=True, default=datetime.datetime.now())

    def save(self, *args, **kwargs):
        if self.SenderAccount== self.ReceiverAccount:
            raise Exception("InvalidTransaction")
        if (len(str(self.SenderAccount)) != 10) or (len(str(self.ReceiverAccount)) != 10):
            raise Exception("InvalidAccountNumber")
        if User.objects.get(accountNo=self.SenderAccount).balance<=self.Amount:
            raise Exception("InsufficientBalance")
        else:
            self.transferMoney()
            super().save(self, *args, **kwargs)
    
    def transferMoney(self):
        senderAcc = User.objects.get(accountNo=self.SenderAccount)
        senderAcc.update(set__balance=senderAcc.balance-self.Amount)
        recieverAcc = User.objects.get(accountNo=self.ReceiverAccount)
        recieverAcc.update(set__balance=recieverAcc.balance+self.Amount)

#print(__name__)


if __name__ == "__main__":
    mongoengine.connect("Authorization")
    #user=User(username="Sarvesh67", password=bcrypt.hashpw("qwerty".encode('utf-8'),bcrypt.gensalt()), DOB=datetime.datetime.today() , aadhar=284904783651, address="Bits Goa")
    #user.save()
    newtransfer = Transfer(SenderAccount=1234567897, ReceiverAccount=1234567898, Amount= 1000, SenderIP = "255.100.50.2")
    newtransfer.save()


  
