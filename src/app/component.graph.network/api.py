orm = wiz.model("orm")
dataset_db = orm.use("dataset")

def load():
    rows = dataset_db.rows(fields="id,title")

    for i in range(len(rows)):
        rows[i]['url'] = "/dashboard/device/" + str(rows[i]['id'])
    
    wiz.response.status(200, rows)