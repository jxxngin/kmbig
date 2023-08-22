import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'survey_group'

    id = pw.IntegerField(primary_key=True)
    survey_id = pw.CharField(max_length=8)
    survey_name = base.TextField()
    logo = base.TextField()
    created = pw.DateTimeField()
    updated = pw.DateTimeField()