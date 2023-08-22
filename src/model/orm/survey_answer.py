import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'survey_answer'

    id = pw.IntegerField(primary_key=True)
    respondent_id = pw.CharField(max_length=12)
    respondent = pw.CharField(max_length=16)
    survey_id = pw.CharField(max_length=8)
    question_id = pw.IntegerField()
    question_sub = pw.CharField(max_length=2)
    answer = pw.IntegerField()
    created = pw.DateTimeField()
    updated = pw.DateTimeField()