import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'files'

    id = pw.IntegerField(primary_key=True, index=True)
    dataset_id = pw.CharField(max_length=32)
    name = pw.CharField(max_length=128)
    year = pw.CharField(max_length=8)
    filepath = base.TextField()
    rows = pw.IntegerField()
    size = pw.IntegerField()
    created = pw.DateTimeField()