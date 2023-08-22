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
    name = storage.list()[0]
    filepath = storage.abspath(name)

    # name = filepath.split('/')[-1]
    filename, fileExtension = os.path.splitext(name)
    if fileExtension == '.xlsx':
        df = pd.read_excel(filepath, engine='openpyxl')
    elif fileExtension == '.csv':
        df = pd.read_csv(filepath, encoding='utf8')

    tongue = dict()

    # LIGHTRED_INDEX count
    tongue['lightred'] = df['LIGHTRED_INDEX']
    df_clean = pd.DataFrame({'lightred': tongue['lightred']}).dropna()

    lightred = [0, 0, 0]
    lightred[0] = (df_clean['lightred'] <= 0.33).sum()
    lightred[1] = ((df_clean['lightred'] > 0.33) & (df_clean['lightred'] < 0.67)).sum()
    lightred[2] = (df_clean['lightred'] >= 0.67).sum()

    # COATED_TONGUE_INDEX
    tongue['coated'] = df['COATED_TONGUE_INDEX']
    df_clean = pd.DataFrame({'coated': tongue['coated']}).dropna()

    coated = [0, 0, 0]
    coated[0] = (df_clean['coated'] <= 0.33).sum()
    coated[1] = ((df_clean['coated'] > 0.33) & (df_clean['coated'] < 0.67)).sum()
    coated[2] = (df_clean['coated'] >= 0.67).sum()

    # BLUEPURPLE_INDEX count
    tongue['bluepurple'] = df['BLUEPURPLE_INDEX']
    df_clean = pd.DataFrame({'bluepurple': tongue['bluepurple']}).dropna()

    bluepurple = [0, 0, 0]
    bluepurple[0] = (df_clean['bluepurple'] <= 0.5).sum()
    bluepurple[1] = (df_clean['bluepurple'] > 0.5).sum()

    # TOOTH_MARK_INDEX count
    tongue['toothmask'] = df['TOOTH_MARK_INDEX']
    df_clean = pd.DataFrame({'toothmask': tongue['toothmask']}).dropna()

    toothmask = [0, 0, 0]
    toothmask[0] = (df_clean['toothmask'] <= 15).sum()
    toothmask[1] = (df_clean['toothmask'] > 15).sum()

    label = list()
    value = dict()
    value['lightred'] = lightred
    value['coated'] = coated
    value['bluepurple'] = bluepurple
    value['toothmask'] = toothmask

    result = dict()
    result['label'] = label
    result['value'] = value
    fs.write.pickle("cache_graph.pkl", result)

    wiz.response.status(200, result)