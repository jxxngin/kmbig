import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'share_request_confirm'

    id = pw.IntegerField(primary_key=True)
    doc_id = pw.IntegerField()
    dataset_name = pw.CharField(max_length=128)
    expert = pw.CharField(max_length=32)
    expert_id = pw.CharField(max_length=32)
    status = pw.CharField(max_length=32)
    comment = base.TextField()
    updated = pw.DateTimeField()