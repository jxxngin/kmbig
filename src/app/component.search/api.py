orm = wiz.model("orm")
datasetDB = orm.use("dataset")

def tag():
    rows = datasetDB.rows(fields="title")
    res = list(map(lambda x: x['title'], rows))
    wiz.response.status(200, res)

def wrap():
    rows = datasetDB.rows(fields='title', orderby='download_count', order='DESC')
    res = list(map(lambda x: x['title'], rows))
    wiz.response.status(200, res)

def log():
    text = wiz.request.query("text", True)
    wiz.model('orm').use('log_search').search_log(text)
    wiz.response.status(200)