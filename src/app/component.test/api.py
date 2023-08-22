import os
import pandas as pd
def fileInfo():
    dataset_id = wiz.request.query('id', True)
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

    wiz.response.status(200, {'means': means, 'labels': labels})