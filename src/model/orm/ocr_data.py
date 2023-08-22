import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'ocr_data'

    id = pw.IntegerField(primary_key=True)
    ocr_id = pw.CharField(max_length=16)
    question_id = pw.IntegerField()
    question_sub = pw.CharField(max_length=2)
    question_name = base.TextField()
    result = pw.IntegerField()
    page = pw.IntegerField()
    pos = base.TextField()
    created = pw.DateTimeField()
    updated = pw.DateTimeField()