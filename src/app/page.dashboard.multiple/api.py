def load():
    dashboard_category = wiz.request.query("id", True)
    dashboard_db = wiz.model('orm').use('dashboard')
    dashboard_row = dashboard_db.get(title=dashboard_category, fields="id,title,category,content")

    db = wiz.model('orm').use('dataset')
    rows = db.rows(fields="id,title",orderby="title",category=dashboard_row["title"])
    
    wiz.response.status(200, {'dashboard_row':dashboard_row, 'dataset_row':rows})