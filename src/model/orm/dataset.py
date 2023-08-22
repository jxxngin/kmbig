import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'dataset'

    num = pw.IntegerField(primary_key=True)
    id = pw.CharField(max_length=32)
    title = pw.CharField(max_length=192)
    category = pw.CharField(max_length=32)
    filetype = pw.CharField(max_length=32)
    filepath = pw.CharField(max_length=192)
    period = pw.CharField(max_length=64)
    schema = base.TextField()
    summary = base.TextField()
    content = base.TextField()
    tags = base.TextField()
    visibility = pw.CharField(max_length=8)
    identification = pw.IntegerField()
    department = pw.CharField(max_length=64)
    main_manager_name = pw.CharField(max_length=20)
    main_manager_email = pw.CharField(max_length=192)
    sub_manager_name = pw.CharField(max_length=20)
    sub_manager_email = pw.CharField(max_length=192)
    view_count = pw.IntegerField()
    download_count = pw.IntegerField()
    favorite_count = pw.IntegerField()
    thumbup_count = pw.IntegerField()
    created = pw.DateTimeField(index=True)
    updated = pw.DateTimeField(index=True)