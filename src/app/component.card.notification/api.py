from datetime import datetime, timedelta

orm = wiz.model("orm")
share_request = orm.use("share_request")
share_request_confirm = orm.use("share_request_confirm")
notification = orm.use("notification")
user = orm.use("user")
wiz.session = wiz.model("session").use()

def load():
    id = wiz.session.get("id")

    result = []
    one_week_ago = datetime.now() - timedelta(weeks=1)
    
    # 공유 요청
    rows = share_request.rows(user_id=id, orderby="updated", order="DESC", fields="id,dataset_name,status,updated")
    request_rows = []

    for i in range(len(rows)):
        rows[i]['title'] = "데이터셋 공유 요청"
        status = rows[i]['status']
        if notification.get(request_id=rows[i]['id']) == None:
            data = dict()
            data['user'] = id
            data['request_id'] = rows[i]['id']
            data['status'] = rows[i]['status']
            notification.insert(data)
        elif notification.get(request_id=rows[i]['id'], status=rows[i]['status']) == None:
            data = dict()
            data['status'] = rows[i]['status']
            data['show'] = 0
            notification.update(data, request_id=rows[i]['id'])

        noti = notification.get(request_id=rows[i]['id'], fields="status,show,updated")
        rows[i]['show'] = noti['show']
        
        if noti['updated'] < one_week_ago and rows[i]['show'] == 1:
            break
        else:
            if status == "request":
                rows[i]['status_name'] = "접수"
                rows[i]['content'] = "귀하의 \'" + rows[i]['dataset_name'] + "\'에 대한 공유 요청이 접수되었습니다."  
            elif status == "process":
                rows[i]['status_name'] = "심사중"
                rows[i]['content'] = "귀하의 \'" + rows[i]['dataset_name'] + "\'에 대한 공유 요청이 심사중 입니다."
            elif status == "allow":
                rows[i]['status_name'] = "승인"
                rows[i]['content'] = "귀하의 \'" + rows[i]['dataset_name'] + "\'에 대한 공유 요청이 승인되었습니다."
            elif status == "reject":
                rows[i]['status_name'] = "거절"
                rows[i]['content'] = "귀하의 \'" + rows[i]['dataset_name'] + "\'에 대한 공유 요청이 거절되었습니다."
            else:
                wiz.response.status(400)
            request_rows.append(rows[i])

    # 전문가 공유 심사
    rows = share_request_confirm.rows(expert_id=id, status="process", orderby="updated", order="DESC", fields="id,doc_id,updated")
    expert_rows = []

    for i in range(len(rows)):
        rows[i]['title'] = "전문가 심사 요청"
        if notification.get(expert_id=rows[i]['id']) == None:
            data = dict()
            data['user'] = id
            data['expert_id'] = rows[i]['id']
            notification.insert(data)
        
        noti = notification.get(expert_id=rows[i]['id'], fields="show,updated")
        rows[i]['show'] = noti['show']

        if noti['updated'] < one_week_ago and rows[i]['show'] == 1:
            break
        else:
            request = share_request.get(id=rows[i]['doc_id'], fields="user_id,dataset_name")
            username = user.get(id=request['user_id'], field="name")["name"]
            rows[i]['status'] = "process"
            rows[i]['status_name'] = "심사"
            rows[i]['content'] = "사용자 " + username + "님의 " + request['dataset_name'] + " 데이터셋 공유 신청에 대한 전문가 심사가 요청되었습니다."
            expert_rows.append(rows[i])

    combined = request_rows + expert_rows
    result = sorted(combined, key=lambda x: x['updated'], reverse=True)

    wiz.response.status(200, result)

def update():
    id = wiz.request.query("id")

    data = dict()
    data['show'] = 1

    if notification.get(request_id=id) != None:
        notification.update(data, request_id=id)
    elif notification.get(expert_id=id) != None:
        notification.update(data, expert_id=id)
    else:
        wiz.response.status(400)

    wiz.response.status(200)