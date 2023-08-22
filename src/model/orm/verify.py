import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    id = pw.IntegerField(primary_key=True)
    email = pw.CharField(max_length=192)
    code = pw.CharField(max_length=6)
    status = pw.CharField(max_length=8)
    created = pw.DateTimeField()
    updated = pw.DateTimeField()

    class Meta:
        db_table = 'verify'
        # primary_key = pw.CompositeKey('code', 'email')