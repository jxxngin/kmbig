import math

def load():
    mode = wiz.request.query("mode", True)
    page = wiz.request.query("page", 1)
    page = int(page)

    user_id = wiz.session.get('id')
    db = wiz.model('orm').use('share_request_confirm')
    userDB = wiz.model('orm').use('user')
    shareDB = wiz.model('orm').use('share_request')

    if mode == "default":
        rows = db.rows(expert_id=user_id, page=page, dump=10)
        cnt = db.count(expert_id=user_id)
    else:
        rows = db.rows(expert_id=user_id, status=mode, page=page, dump=10)
        cnt = db.count(expert_id=user_id, status=mode)

    lastpage = math.ceil(cnt/10)

    for row in rows:
        if row['status'] == 'allow':
            row['status_name'] = '승인'
            row['status_class'] = 'btn-allow'
        elif row['status'] == 'reject':
            row['status_name'] = '거절'
            row['status_class'] = 'btn-reject'
        elif row['status'] == 'process':
            row['status_name'] = '심사중'
            row['status_class'] = 'btn-process'
        elif row['status'] == 'stop':
            row['status_name'] = '중단'
            row['status_class'] = 'btn-stop'

        row['username'] = userDB.get(id=user_id, fields='username')['username']
        print('id : ', row['doc_id'])
        shareRow = shareDB.get(id=row['doc_id'], fields="purpose,created,deadline")
        row['purpose'] = shareRow['purpose']
        row['created'] = shareRow['created']
        row['deadline'] = shareRow['deadline']

    wiz.response.status(200, {"rows":rows, "lastpage":lastpage})
