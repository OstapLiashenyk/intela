from peewee import *

# Define your database connection
draft_database = SqliteDatabase('draft.db')

# Define your base model
class BaseModel(Model):
    class Meta:
        database = draft_database
        legacy_table_names = False

# Define your Peewee model with the required fields
class TestsS(BaseModel):
    id = IntegerField()
    posted = DateTimeField(null=True)
    jobFunctionSough = CharField(null=True)
    desiredIndustry = CharField(null=True)
    location = CharField(null=True)
    objective = TextField(null=True)
    experience = TextField(null=True)
    education = TextField(null=True)
    affiliations = TextField(null=True)
    skills = TextField(null=True)
    additionalInformation = TextField(null=True)
    reference = TextField(null=True)

    class Meta:
        table_name = 'jobSpider'
