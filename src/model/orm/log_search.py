import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'log_search'

    id = pw.IntegerField(primary_key=True)
    user_id = pw.CharField(max_length=20)
    search_ip = pw.CharField(max_length=16)
    search_text = pw.CharField(max_length=64)
    search_time = pw.DateTimeField()