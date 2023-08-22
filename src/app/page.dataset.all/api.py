def load():
    dashboard_id = wiz.request.query("id", True)
    dashboard_db = wiz.model('orm').use('dashboard')
    dashboard_row = dashboard_db.get(category=dashboard_id, fields="id,category,content")

    db = wiz.model('orm').use('dataset')
    rows = db.rows(fields="id,title",orderby="title")
    
    wiz.response.status(200, {'dashboard_row':dashboard_row, 'dataset_row':rows})