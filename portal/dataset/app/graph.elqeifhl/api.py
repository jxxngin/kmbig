import os
import pandas as pd

def fileInfo():
    dataset_id = wiz.request.query('id', True)

    fs = wiz.model("fs").use(f"files/{dataset_id}/cache")
    if fs.exists("cache_graph.pkl"):
        result = fs.read.pickle("cache_graph.pkl")
        wiz.response.status(200, result)

    db = wiz.model('orm').use('dataset')
    filepath = db.get(id=dataset_id, fields="filepath")['filepath']

    fname = filepath.split('/')[-1]
    filename, fileExtension = os.path.splitext(fname)
    if fileExtension == '.xlsx':
        df = pd.read_excel(filepath, engine='openpyxl')
    elif fileExtension == '.csv':
        df = pd.read_csv(filepath, encoding='utf8')

    measure1 = df['MEASURE1'].mean()
    measure2 = df['MEASURE2'].mean()
    measure3 = df['MEASURE3'].mean()
    means = [measure1, measure2, measure3]
    labels = ['1회차 측정', '2회차 측정', '3회차 측정']

    result = dict()
    result['means'] = means
    result['labels'] = labels
    fs.write.pickle("cache_graph.pkl", result)

    wiz.response.status(200, result)