def pages():
    # print('query : ', wiz.request.query())
    page_id = wiz.request.query('page', True)
    db = wiz.model('orm').use('pages')
    row = db.get(pages=page_id, fields='pages,content,filepath')
    wiz.response.status(200, row)