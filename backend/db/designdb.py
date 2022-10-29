from bson import ObjectId
#design the database
from mongoengine import *
from pkg_resources import require


class Investments(EmbeddedDocument):
    id = ObjectId
    amount = IntField
    length_investment = DateField(required=True)

class Payment(EmbeddedDocument):
    account_number = IntField()
    security_code = IntField() 

class User(Document):
    id = ObjectIdField(required=True)
    name = StringField(max_length=50)
    address = StringField()
    verification = BooleanField()
    investments = EmbeddedDocumentField(Investments)
    payment = EmbeddedDocumentField(Payment)
    

class Project(Document):
    id = ObjectIdField(required=True)
    general_info = StringField()
    total_funds = IntField()
    dates_until_expired = DateField(required=True)







