def file_info():
    dataset_id = wiz.request.query('id', True)
    category = wiz.request.query('category', True)
    file_db = wiz.model('orm').use('files')
    file_info = file_db.get(dataset_id=dataset_id, fields='rows')

    wiz.response.status(200, file_info)