import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'macro'

    num = pw.IntegerField(primary_key=True)
    id = pw.CharField(max_length=12)
    title = pw.CharField(max_length=192)
    namespace = pw.CharField(max_length=64)
    filetype = base.TextField()
    content = base.TextField()
    code = base.TextField()
    created = pw.DateTimeField(index=True)
    updated = pw.DateTimeField(index=True)