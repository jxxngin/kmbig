import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'board'

    id = pw.IntegerField(primary_key=True, index=True)
    parent_id = pw.IntegerField()
    priority = pw.IntegerField()
    user_id = pw.CharField(max_length=20)
    category = pw.CharField(max_length=20)
    title = pw.CharField(max_length=128)
    comment = pw.IntegerField()
    content = base.TextField()
    files = base.TextField()
    created = pw.DateTimeField()
    updated = pw.DateTimeField()