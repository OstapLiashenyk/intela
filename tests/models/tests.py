from peewee import *
from connections import draft_database
from playhouse.mysql_ext import JSONField

class BaseModel(Model):
    class Meta:
        database = draft_database
        legacy_table_names = False

class TestsS(BaseModel):
    id = CharField(primary_key=True, max_length=64)
    title = CharField()
    level = CharField(max_length=32, null=True)
    avg_score = IntegerField(null=True)
    attempts = IntegerField(null=True)
    topic = CharField()
    class Meta:
        table_name = 'studytonight_tests'

class TestQuestionsS(BaseModel):
    id = CharField(primary_key=True, max_length=64)
    question = TextField()
    question_html = TextField()
    options = TextField(null=True)
    options_html = TextField(null=True)
    answer = JSONField()# Подивитись
    test = ForeignKeyField(TestsS, backref='test')
    class Meta:
        table_name = 'studytonight_test_questions'

class QnrSingleSelectItem(BaseModel):
    id = CharField(primary_key=True, max_length=32)
    skill = CharField(max_length=32)
    score = SmallIntegerField()
    is_puzzle = BooleanField(default=True)
    is_exam = BooleanField(default=True)
    question = TextField()
    acceptable_duration = IntegerField(null=True)
    article = TextField(null=True)
    read_duration = IntegerField(null=True)
    explanation = TextField(null=True)
    recommendation = TextField(null=True)
    source = CharField(max_length=64, null=True)
    class Meta:
        table_name = 'qnr_single_select_item'

class QnrSingleAnswerOption(BaseModel):
    qnr_item = ForeignKeyField(QnrSingleSelectItem, backref='qnr_item')
    num = SmallIntegerField()
    is_correct = BooleanField(default=False)
    text = CharField(max_length=1024)
    class Meta:
        primary_key = CompositeKey('qnr_item', 'num')# Подивитись
        table_name = 'qnr_single_answer_option'
