def fileInfo():
    id = wiz.request.query("id", True)
    db = wiz.model('orm').use('files')
    rows = db.rows(dataset_id=id, fields="year,rows")

    wiz.response.status(200, rows)