import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'survey_question'

    id = pw.IntegerField(primary_key=True)
    survey_id = pw.CharField(max_length=8)
    question_id = pw.IntegerField()
    question_sub = pw.CharField(max_length=2)
    question_name = base.TextField()
    result = pw.IntegerField()
    created = pw.DateTimeField()
    updated = pw.DateTimeField()