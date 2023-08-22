import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'survey'

    id = pw.CharField(primary_key=True, max_length=16)
    title = pw.CharField(max_length=128)
    description = base.TextField()
    question_file = base.TextField()
    answer_file = base.TextField()
    created = pw.DateTimeField()
    updated = pw.DateTimeField()