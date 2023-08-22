import json
import os
import pandas as pd
import simplejson

sessionID = wiz.session.get("id")
def load():
    formId = wiz.request.query("id", True)

    confirmDB = wiz.model('orm').use('share_request_confirm')
    confirmRow = confirmDB.get(id=formId, fields="doc_id,expert_id,status,comment")
    
    if confirmRow is None or sessionID != confirmRow['expert_id']:
        wiz.response.status(300, True)
    
    status = confirmRow['status']
    docID = confirmRow['doc_id']
    
    share_db = wiz.model('orm').use('share_request')
    row = share_db.get(id=docID)
    row['expert_status'] = status
    row['comment'] = confirmRow['comment']
    row['expert'] = confirmRow['expert_id']

    dataDB = wiz.model('orm').use('dataset')
    category = dataDB.get(id=row['dataset_id'], fields="category")['category']
    if category == "기기":
        category = "device"
    row['category'] = category

    # 공유 요청자 정보
    userDB = wiz.model('orm').use('user')
    user = userDB.get(id=row['user_id'], fields="name")['name']
    row['user'] = user

    # 심사 상태
    if row['expert_status'] == 'stop':
        row['status_name'] = '중단'
        row['status_class'] = 'btn-stop'
    elif row['expert_status'] == 'allow':
        row['status_name'] = '승인'
        row['status_class'] = 'btn-allow'
    elif row['expert_status'] == 'reject':
        row['status_name'] = '거절'
        row['status_class'] = 'btn-reject'
    elif row['expert_status'] == 'process':
        row['status_name'] = '심사중'
        row['status_class'] = 'btn-process'
            
    # 데이터 미리보기
    fs = wiz.model("fs").use(f"dataset/{row['dataset_id']}/share/{docID}/cache")
    preview = fs.read.pickle("cache_preview.pkl")
    dataDB = wiz.model("orm").use("dataset")
    dataRow = dataDB.get(id=row['dataset_id'], fields="schema")
    preview["schema"] = dataRow['schema']

    wiz.response.status(200, {"info":row, "preview": preview})

def update():
    formID = wiz.request.query("form", True)
    status = wiz.request.query("status", True)
    comment = wiz.request.query("comment", True)
    confirmDB = wiz.model("orm").use("share_request_confirm")
    
    expertUpdate = dict()
    expertUpdate['id'] = formID
    expertUpdate['status'] = status
    expertUpdate['comment'] = comment
    confirmDB.update(expertUpdate, id=formID)

    # 관리자에게 공유 심사 완료 이메일 전송
    confirmInfo = confirmDB.get(id=formID, fields="id,doc_id,dataset_name,expert")
    shareDB = wiz.model('orm').use('share_request')
    userID = shareDB.get(id=confirmInfo['doc_id'], fields="user_id")['user_id']
    userDB = wiz.model('orm').use('user')
    userName = userDB.get(id=userID, fields="name")['name']
    url = "https://kmbig-admin.seasonsoft.net/share/list/view/"+str(confirmInfo['doc_id'])
    message = f"</br></br>전문가 {confirmInfo['expert']}님께서 사용자 {userName}님의 {confirmInfo['dataset_name']} 데이터셋 공유(활용) 요청에 대한 심사를 완료하였습니다.</br></br>심사를 결과를 확인하여 주시기 바랍니다.</br></br><a href='{url}' target='_blank'>전문가 심사 결과 확인하기</a>"
    smtp = wiz.model("portal/season/smtp").use()
    smtp.send(
        "kwon3286@season.co.kr",
        template="default",
        title="데이터셋 공유 신청",
        message=message)

    wiz.response.status(200, True)