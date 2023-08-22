import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'log_access'

    id = pw.IntegerField(primary_key=True)
    session_id = pw.CharField(max_length=192)
    user_id = pw.CharField(max_length=20)
    namespace = pw.CharField(max_length=128)
    access_ip = pw.CharField(max_length=16)
    access_time = pw.DateTimeField()
    full_url = pw.TextField()
    useragent = pw.TextField()