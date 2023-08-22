import os
import season
import datetime
import json
import simplejson
import zipfile
import tempfile

def load():
    user_id = wiz.session.get('id')
    docId = wiz.request.query("id", True)

    share_db = wiz.model('orm').use('share_request')
    row = share_db.get(id=docId)
    
    if row is None or user_id != row['user_id']:
        wiz.response.status(300, True)

    dataDB = wiz.model('orm').use('dataset')
    category = dataDB.get(id=row['dataset_id'], fields="category")['category']
    if category == "기기":
        category = "device"
    row['category'] = category

    userDB = wiz.model('orm').use('user')
    user = userDB.get(id=row['user_id'], fields="name")['name']
    row['user'] = user

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
            
    wiz.response.status(200, row)

def download():
    dataId = wiz.request.query('id', True)
    dataName = wiz.request.query('title', True)
    path = f"dataset/{dataId}/manage/current"
    storage = wiz.model("storage").use()

    # zip 파일로 다운로드
    filepath = storage.abspath(path)
    filename = dataName + ".zip"
    zippath = os.path.join(tempfile.gettempdir(), filename)
    
    try:
        os.remove(zippath)
    except:
        pass
    
    os.makedirs(os.path.dirname(zippath), exist_ok=True)
    zipdata = zipfile.ZipFile(zippath, 'w')
    for folder, _, files in os.walk(filepath):
        for file in files:
            # 기존 데이터셋 파일 제거
            if "export" in file: 
                continue
            zipdata.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), filepath), compress_type=zipfile.ZIP_DEFLATED)
    
    # 필터 적용된 파일 추가
    docID = wiz.request.query("docID", True)
    filterPath = wiz.model("storage").use(f"dataset/{dataId}/share/{docID}").abspath()
    for folder, _, files in os.walk(filterPath):
        for file in files:
            if "filter" in file:
                zipdata.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), filterPath), compress_type=zipfile.ZIP_DEFLATED)
    
    zipdata.close()
    filepath = zippath

    # DB 데이터셋 다운로드 수
    data_db = wiz.model('orm').use('dataset')
    data = data_db.get(id=dataId, fields="id,title,download_count")
    data['download_count'] = data['download_count'] + 1
    data_db.update(data, id=dataId)

    wiz.response.download(filepath, as_attachment=True, filename=filename)

def drive():
    dataID = wiz.request.query("id", True)
    dataName = wiz.request.query("name", True)
    userID = wiz.session.get("id")
    docID = wiz.request.query("docID", True)

    storage_u = wiz.model("storage").use(f"user/{userID}/{dataName}")
    BASEPATH_u = storage_u.abspath()
    if len(storage_u.list()) == 0:
        storage_d = wiz.model("storage").use(f"dataset/{dataID}/manage/current")
        BASEPATH_d = storage_d.abspath()

        storage_u.copy(BASEPATH_d, BASEPATH_u)

        # 필터 적용된 파일 추가
        lsU = storage_u.list()
        for u in lsU:
            # 원본 데이터 파일 제거
            if "xlsx" in u:
                storage_u.remove(u)

    storage_d = wiz.model("storage").use(f"dataset/{dataID}/share/{docID}")
    lsD = storage_d.list()
    for f in lsD:
        if "filter" in f:
            lsF = f
            break

    filepath = os.path.join(storage_d.abspath(), lsF)
    filepath2 = os.path.join(BASEPATH_u, lsF)
    storage_u.copy(filepath, filepath2)

    wiz.response.status(200, True)