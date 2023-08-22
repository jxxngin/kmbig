import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'drive'

    id = pw.IntegerField(primary_key=True)
    user_id = pw.CharField(max_length=128)
    filename = pw.CharField(max_length=128)
    filepath = pw.CharField(max_length=256)
    created = pw.DateTimeField(index=True)