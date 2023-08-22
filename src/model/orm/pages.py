import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'pages'

    id = pw.IntegerField(primary_key=True, index=True)
    pages = pw.CharField(max_length=32)
    content = base.TextField()
    filepath = pw.CharField(max_length=64)
    updated = pw.DateTimeField(index=True)