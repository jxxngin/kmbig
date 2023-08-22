import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'share_request'

    id = pw.IntegerField(primary_key=True)
    user_id = pw.CharField(max_length=32)
    dataset_id = pw.CharField(max_length=32)
    dataset_name = pw.CharField(max_length=32)
    purpose = pw.CharField(max_length=32)
    content = base.TextField()
    filter = base.TextField()
    status = pw.CharField(max_length=32)
    created = pw.DateTimeField()
    updated = pw.DateTimeField()
    deadline = pw.DateField()