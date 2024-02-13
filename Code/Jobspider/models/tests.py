from peewee import *
from connections import draft_database
from playhouse.mysql_ext import JSONField

class BaseModel(Model):
    class Meta:
        database = draft_database
        legacy_table_names = False

class TestsS(BaseModel):

    class Meta:
        table_name = ''




