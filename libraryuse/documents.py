from tastypie.utils.timezone import now
from django.db import models
from mongoengine import Document
from mongoengine import fields


class Visits(Document):
    id = fields.StringField()
    visit_time = fields.DateTimeField()
    location = fields.StringField()

    # This doesn't have to be set as long as all the fields line up.
    # Seems like a good idea to keep it.
    meta = {'collection': 'test'}
    
class VisitMinute(Document):
    id = fields.StringField()
    visit_time = fields.DateTimeField()
    location = fields.StringField()

    meta = {'collection': 'visit_minute'}
    
class VisitHalfHour(Document):
    id = fields.StringField()
    visit_time = fields.DateTimeField()
    location = fields.StringField()

    meta = {'collection': 'visit_halfhour'}
    
class VisitCountHalfHour(Document):
    id = fields.StringField()
    visit_time = fields.DateTimeField()
    epoch_visit_time = fields.IntField()
    location = fields.StringField()
    count = fields.IntField()

    meta = {'collection': 'visitcount_halfhour'}
