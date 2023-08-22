import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'notification'

    id = pw.IntegerField(primary_key=True)
    user = pw.CharField(max_length=20)
    request_id = pw.IntegerField()
    expert_id = pw.IntegerField()
    status = pw.CharField(max_length=16)
    show = pw.IntegerField()
    updated = pw.DateTimeField()