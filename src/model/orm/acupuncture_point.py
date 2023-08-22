import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'acupuncture_point'

    id = pw.IntegerField(primary_key=True, index=True)
    title = pw.CharField(max_length=20)
    img = pw.CharField(max_length=128)
    cnt = pw.IntegerField()