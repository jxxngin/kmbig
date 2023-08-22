import os
import pandas as pd
import json
import simplejson
import math
from openpyxl import load_workbook
from collections import Counter

def fileInfo():
    dataset_id = wiz.request.query('id', True)

    fs = wiz.model("fs").use(f"files/{dataset_id}/cache")
    fs = wiz.model("fs").use(f"dataset/{dataset_id}/cache")
    if fs.exists("cache_graph.pkl"):
        result = fs.read.pickle("cache_graph.pkl")
        wiz.response.status(200, result)

    db = wiz.model('orm').use('dataset')
    filepath = db.get(id=dataset_id, fields="filepath")['filepath']

    name = filepath.split('/')[-1]
    filename, fileExtension = os.path.splitext(name)
    if fileExtension == '.xlsx':
        df = pd.read_excel(filepath, engine='openpyxl')
    elif fileExtension == '.csv':
        df = pd.read_csv(filepath, encoding='utf8')

    color_df = df['COLOR']
    color_ls = list(color_df)
    color_ls = [int(x) for x in color_ls if math.isnan(x) == False]
    color_cnt = Counter(color_ls)

    color_result = dict(sorted(color_cnt.items()))
    label = list()
    value = list()

    for key in color_result.keys():
        label.append(str(key))
        value.append(color_result[key])

    result = dict()
    result['label'] = label
    result['value'] = value
    fs.write.pickle("cache_graph.pkl", result)
    
    wiz.response.status(200, result)