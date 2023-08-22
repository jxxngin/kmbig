import os
import season
import datetime
import json
import simplejson
import zipfile
import tempfile
import pandas as pd
from openpyxl import load_workbook

import pandas as pd
import numpy as np

wiz.session = wiz.model('session').use()
user_id = wiz.session.get('id')

def info():
    category = wiz.request.query('category', True)
    dataset_id = wiz.request.query('id', True)
    db = wiz.model('orm').use('dataset')
    row = db.get(id=dataset_id)

    wiz.model('orm').use('log_access').upsert_log(f"/dashboard/{category}/{dataset_id}", 1)
    count = dict()
    count['view_count'] = wiz.model('orm').use('log_access').count(namespace=f"/dashboard/{category}/{dataset_id}")
    db.update(count, id=dataset_id)

    wiz.response.status(200, row)

def shareInfo():
    dataID = wiz.request.query("id", True)
    shareDB = wiz.model('orm').use('share_request')
    rows = shareDB.rows(user_id=user_id, dataset_id=dataID, order="DESC", orderby="updated", fields="id,content,purpose,status,dataset_name,filter,updated")

    if rows is None:
        wiz.response.status(201, False)

    for i in range(len(rows)):
        if rows[i]['status'] == 'request':
            rows[i]['status_name'] = '접수'
            rows[i]['status_class'] = 'btn-request'
        elif rows[i]['status'] == 'allow':
            rows[i]['status_name'] = '승인'
            rows[i]['status_class'] = 'btn-allow'
        elif rows[i]['status'] == 'reject':
            rows[i]['status_name'] = '거절'
            rows[i]['status_class'] = 'btn-reject'
        elif rows[i]['status'] == 'process':
            rows[i]['status_name'] = '심사중'
            rows[i]['status_class'] = 'btn-process'

    wiz.response.status(200, rows)

def request():
    dataID = wiz.request.query("id", True)
    dataName = wiz.request.query("name", True)
    purpose = wiz.request.query("purpose", True)
    content = wiz.request.query("content", True)
    userID = wiz.request.query("userID", True)
    filter = wiz.request.query("filter", True)
    filter2 = json.loads(filter)

    # filterResult(dataID, userID, filter2)

    shareDB = wiz.model('orm').use('share_request')
    share = dict()
    share['user_id'] = user_id
    share['dataset_id'] = dataID
    share['dataset_name'] = dataName
    share['purpose'] = purpose
    share['content'] = content
    share['filter'] = filter2
    share['status'] = "request"
    share['created'] = datetime.datetime.now()
    shareDB.insert(share)

    # 관리자에게 공유 심사 요청 이메일 전송
    userDB = wiz.model('orm').use('user')
    userName = userDB.get(id=user_id, fields="name")['name']
    shareID = shareDB.get(user_id=user_id, dataset_id=dataID, status="request", fields="id")['id']
    url = "https://kmbig-admin.seasonsoft.net/share/list/view/"+str(shareID)
    message = f"</br></br>사용자 {userName}님께서 {dataName} 데이터셋 공유 신청을 하였습니다.</br></br>공유 심사를 요청드립니다.</br></br><a href='{url}' target='_blank'>데이터셋 공유 심사하러 가기</a>"
    smtp = wiz.model("portal/season/smtp").use()
    smtp.send(
        "jeongcr@season.co.kr",
        template="default",
        title="데이터셋 공유 신청",
        message=message)

    wiz.response.status(200, shareID)

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

def filterResult(dataID, userID, filtered):
    # 파일 추출
    path = f"dataset/{dataID}/manage/current"
    storage = wiz.model("storage").use(path)
    ls = storage.list()
    for one in ls:
        if ")_" in one:
            fname = one
            break

    filepath = storage.abspath(fname)
    filename, fileExtension = os.path.splitext(fname)
    if fileExtension == '.xlsx':
        df = pd.read_excel(filepath, engine='openpyxl')
    elif fileExtension == '.csv':
        df = pd.read_csv(filepath, encoding='utf8')
    
    # 필터 값 추출
    period = [key for key, value in filtered["period"].items() if value is True]
    age = [key for key, value in filtered["age"].items() if value is True]
    sex = [key for key, value in filtered["sex"].items() if value is True]
    sasang = [key for key, value in filtered["sasang"].items() if value is True]
    height1 = filtered['height1']
    height2 = filtered['height2'] 
    weight1 = filtered['weight1']
    weight2 = filtered['weight2'] 

    # 필터 값이 있는 컬럼 중 NaN이 포함된 row 제거
    column = []
    column = [
        "BIRTHDAY" if len(age) > 0 else None,
        "SEX" if len(sex) > 0 else None,
        "SASANG_TY_CODE" if len(sasang) > 0 else None,
        "HEIGHT" if len(height1) > 0 or len(height2) > 0 else None,
        "WEIGHT" if len(weight1) > 0 or len(weight2) > 0 else None
    ]
    column = [col for col in column if col is not None]
    df_without_nan = df.dropna(subset=column).reset_index(drop=True)

    # 생년월일(BIRTHDAY) 컬럼 통해서 연령대 추출
    df_without_nan['age_year'] = df_without_nan['BIRTHDAY'].map(lambda x: int(str(int(x))[:4]) if pd.notnull(x) else None)
    conditions = []
    for i in range(11):
        start_year = 1925 + (i * 10)
        end_year = 1934 + (i * 10)
        condition = df_without_nan['age_year'].between(start_year, end_year)
        conditions.append(condition)
    choices = ['100세 이상', '90대', '80대', '70대', '60대', '50대', '40대', '30대', '20대', '10대', '0~9세']
    df_without_nan['age'] = np.select(conditions, choices, default='기타')

    # 체질 추출
    sa_type_mapping = {'TY': '태양인', 'TE':'태음인', 'SY': '소양인', 'SE': '소음인'}
    df_without_nan['sasang'] = df_without_nan['SASANG_TY_CODE'].map(sa_type_mapping).fillna('기타')

    # 성별 추출
    sex_type_mapping = {'F': '여자', 'M':'남자'}
    df_without_nan['sex'] = df_without_nan['SEX'].map(sex_type_mapping).fillna('기타')

    # 필터 적용
    testH = len(height1) > 0 or len(height2) > 0
    if testH:
        height1 = float(height1) if len(height1) > 0 else 0
        height2 = float(height2) if len(height2) > 0 else 300

    testW = len(weight1) > 0 or len(weight2) > 0
    if testW:
        weight1 = float(weight1) if len(weight1) > 0 else 0
        weight2 = float(weight2) if len(weight2) > 0 else 300

    df_without_nan['period'] = df_without_nan['LAST_UPDT_PNTTM'].dt.strftime('%Y')
    df_without_nan = df_without_nan[df_without_nan['period'].isin(period)] if len(period) > 0 else df_without_nan
    df_without_nan = df_without_nan[df_without_nan['sex'].isin(sex)] if len(sex) > 0 else df_without_nan
    df_without_nan = df_without_nan[df_without_nan['age'].isin(age)] if len(age) > 0 else df_without_nan
    df_without_nan = df_without_nan[df_without_nan['sasang'].isin(sasang)] if len(sasang) > 0 else df_without_nan
    df_without_nan = df_without_nan[df_without_nan['HEIGHT'].between(height1, height2)] if testH else df_without_nan
    df_without_nan = df_without_nan[df_without_nan['WEIGHT'].between(weight1, weight2)] if testW else df_without_nan

    # 다중 컬럼을 삭제
    columns_to_drop = ['period', 'sex', 'age', 'sasang', 'age_year']
    filtered_df = df_without_nan.drop(columns=columns_to_drop).reset_index(drop=True)
    # filtered_df = filtered_df.drop(filtered_df.columns[0], axis=1)

    # 필터 적용 데이터셋 저장
    savePath = f"dataset/{dataID}/share"
    storage = wiz.model("storage").use(savePath)
    if not storage.exists(userID):
        storage.makedirs(userID)
    saveName = userID + "/" + filename + "_filter.xlsx"
    storage.write.excel(saveName, filtered_df)

    # 필터 적용 데이터셋 -> head(5) cache 저장
    dfCache = filtered_df.head(5)
    dfCache = dfCache.fillna('')
    dfCache = dfCache.astype(dtype='str')
    dfCache = dfCache.to_dict(orient='records')
    dfCache = simplejson.dumps(dfCache, ignore_nan=True)
    dfCache = json.loads(dfCache)

    fs = wiz.model("fs").use(f"dataset/{dataID}/share/{userID}/cache")
    fs.write.pickle("cache_preview.pkl", dfCache)