import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'ocr_info'

    id = pw.CharField(primary_key=True, max_length=16)
    name = pw.CharField(max_length=128)
    file = base.TextField()
    images = base.TextField()
    created = pw.DateTimeField()
    updated = pw.DateTimeField()