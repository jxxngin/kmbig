import os
import pandas as pd
import json
import simplejson
from openpyxl import load_workbook

def file_info():
    dataset_id = wiz.request.query('id', True)
    # category = wiz.request.query('category', True)

    # fs = wiz.model("fs").use(f"files/{category}/{dataset_id}/cache")
    # fs = wiz.model("fs").use(f"files/{dataset_id}/cache")
    fs = wiz.model("fs").use(f"dataset/{dataset_id}/cache")
    if fs.exists("cache_preview_add.pkl"):
        result = fs.read.pickle("cache_preview_add.pkl")
        wiz.response.status(200, result)

    # file_db = wiz.model('orm').use('files')
    # file_info = file_db.get(dataset_id=dataset_id, fields='name,filepath,rows')
    # name = file_info['name']
    # filepath = file_info['filepath']

    # 개인정보 포함된 테스트 더미 데이터
    # path = f"files/{dataset_id}/manage/current"
    path = f"dataset/{dataset_id}/manage/current"
    storage = wiz.model("storage").use(path)
    ls = storage.list()

    for one in ls:
        if ")_" in one:
            name = one
            break
    print("name : ", name)
    filepath = storage.abspath(name)

    filename, fileExtension = os.path.splitext(name)
    if fileExtension == '.xlsx':
        df = pd.read_excel(filepath, engine='openpyxl').head(5)
    elif fileExtension == '.csv':
        df = pd.read_csv(filepath, encoding='utf8').head(5)
    
    df = df.fillna('')
    df = df.astype(dtype='str')
    df = df.to_dict(orient='records')
    df = simplejson.dumps(df, ignore_nan=True)
    df = json.loads(df)

    # result = dict()
    # result['df'] = df
    # result['filename'] = name
    # result['filepath'] = filepath
    # result['file_row'] = file_info['rows']
    fs.write.pickle("cache_preview_add.pkl", df)

    wiz.response.status(200, df)
    # wiz.response.status(200, {'df':df, 'filename':name, 'filepath':filepath, 'file_row':file_info['rows']})