import math

def load():
    mode = wiz.request.query("mode", True)
    page = wiz.request.query("page", 1)
    page = int(page)

    user_id = wiz.session.get('id')
    db = wiz.model('orm').use('share_request')

    if mode == "default":
        rows = db.rows(user_id=user_id, page=page, dump=15, orderby='created', order='DESC')
        cnt = db.count(user_id=user_id)
    else:
        rows = db.rows(user_id=user_id, status=mode, page=page, dump=15, orderby='created', order='DESC')
        cnt = db.count(user_id=user_id, status=mode)

    lastpage = math.ceil(cnt/15)

    for row in rows:
        if row['status'] == 'request':
            row['status_name'] = '접수'
            row['status_class'] = 'btn-request'
        elif row['status'] == 'allow':
            row['status_name'] = '승인'
            row['status_class'] = 'btn-allow'
        elif row['status'] == 'reject':
            row['status_name'] = '거절'
            row['status_class'] = 'btn-reject'
        elif row['status'] == 'process':
            row['status_name'] = '심사중'
            row['status_class'] = 'btn-process'

    wiz.response.status(200, {"rows":rows, "lastpage":lastpage})
