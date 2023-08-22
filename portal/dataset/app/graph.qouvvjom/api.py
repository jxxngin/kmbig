import os
import pandas as pd
from openpyxl import load_workbook

def fileInfo():
    dataset_id = wiz.request.query('id', True)

    # fs = wiz.model("fs").use(f"files/{dataset_id}/cache")
    fs = wiz.model("fs").use(f"dataset/{dataset_id}/cache")
    if fs.exists("cache_graph.pkl"):
        result = fs.read.pickle("cache_graph.pkl")
        wiz.response.status(200, result)

    # db = wiz.model('orm').use('dataset')
    # filepath = db.get(id=dataset_id, fields="filepath")['filepath']

    db = wiz.model('orm').use('dataset')
    storage = wiz.model("storage").use(f"dataset/{dataset_id}/manage/current")
    fname = storage.list()[0]
    filepath = storage.abspath(fname)
    
    # fname = filepath.split('/')[-1]
    filename, fileExtension = os.path.splitext(fname)
    if fileExtension == '.xlsx':
        df = pd.read_excel(filepath, engine='openpyxl')
    elif fileExtension == '.csv':
        df = pd.read_csv(filepath, encoding='utf8')

    antigen_df = df[~df['ANTIGEN1'].isna()].loc[:, 'ANTIGEN3':'ANTIGEN93']
    antigen_count = (antigen_df > 0).sum()
    antigen_top = antigen_count.nlargest(10)

    antigen_top = antigen_top.rename(index={
        "ANTIGEN3": "집먼지진드기",
        "ANTIGEN4": "저장진드기",
        "ANTIGEN5": "고양이",
        "ANTIGEN13": "새우",
        "ANTIGEN20": "집먼지",
        "ANTIGEN28": "돼지풀",
        "ANTIGEN32": "수중다리진드기",
        "ANTIGEN39": "향기풀",
        "ANTIGEN40": "우산잔디",
        "ANTIGEN60": "명아주과풀"
    })
    antigen_top = antigen_top.to_dict()
    label = list()
    value = list()

    for key in antigen_top.keys():
        label.append(str(key))
        value.append(antigen_top[key])

    result = dict()
    result['label'] = label
    result['value'] = value
    fs.write.pickle("cache_graph.pkl", result)

    wiz.response.status(200, result)