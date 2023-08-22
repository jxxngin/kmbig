import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'board_comment'

    id = pw.IntegerField(primary_key=True, index=True)
    board_id = pw.IntegerField()
    user_id = pw.CharField(max_length=20)
    content = base.TextField()
    status = pw.CharField(max_length=8)
    created = pw.DateTimeField()
    updated = pw.DateTimeField()