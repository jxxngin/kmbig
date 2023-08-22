import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'dashboard'

    id = pw.IntegerField(primary_key=True)
    title = pw.CharField(max_length=32)
    category = pw.CharField(max_length=32)
    content = base.TextField()
    period = base.TextField()
    filepath = base.TextField()
    created = pw.DateTimeField(index=True)
    updated = pw.DateTimeField(index=True)