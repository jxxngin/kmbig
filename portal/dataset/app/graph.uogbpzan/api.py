import os
import pandas as pd

def fileInfo():
    dataset_id = wiz.request.query('id', True)
    
    # fs = wiz.model("fs").use(f"files/{dataset_id}/cache")
    fs = wiz.model("fs").use(f"dataset/{dataset_id}/cache")
    if fs.exists("cache_graph.pkl"):
        result = fs.read.pickle("cache_graph.pkl")
        wiz.response.status(200, result)

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

    df2 = df[['HEIGHT', 'WEIGHT', 'BMI']]
    df_140 = df2[(df2['HEIGHT'] >= 140.0) & (df2['HEIGHT'] < 150.0)]
    weight_140 = df_140['WEIGHT'].mean()
    bmi_140 = df_140['BMI'].mean()

    df_150 = df2[(df2['HEIGHT'] >= 150.0) & (df2['HEIGHT'] < 160.0)]
    weight_150 = df_150['WEIGHT'].mean()
    bmi_150 = df_150['BMI'].mean()

    df_160 = df2[(df2['HEIGHT'] >= 160.0) & (df2['HEIGHT'] < 170.0)]
    weight_160 = df_160['WEIGHT'].mean()
    bmi_160 = df_160['BMI'].mean()

    df_170 = df2[(df2['HEIGHT'] >= 170.0) & (df2['HEIGHT'] < 180.0)]
    weight_170 = df_170['WEIGHT'].mean()
    bmi_170 = df_170['BMI'].mean()

    df_180 = df2[(df2['HEIGHT'] >= 180.0) & (df2['HEIGHT'] < 190.0)]
    weight_180 = df_180['WEIGHT'].mean()
    bmi_180 = df_180['BMI'].mean()

    df_190 = df2[df2['HEIGHT'] >= 190.0]
    weight_190 = df_190['WEIGHT'].mean()
    bmi_190 = df_190['BMI'].mean()

    weight_means = [weight_140, weight_150, weight_160, weight_170, weight_180, weight_190]
    bmi_means = [bmi_140, bmi_150, bmi_160, bmi_170, bmi_180, bmi_190]
    # labels = ['140cm 이상, 150cm 미만', '150cm 이상, 160cm 미만', '160cm 이상, 170cm 미만', '170cm 이상, 180cm 미만', '180cm 이상, 190cm 미만', '190cm 이상']
    labels = ['140cm ~ 150cm', '150cm ~ 160cm', '160cm ~ 170cm', '170cm ~ 180cm', '180cm ~ 190cm', '190cm 이상']

    result = dict()
    result['weight_means'] = weight_means
    result['bmi_means'] = bmi_means
    result['labels'] = labels
    fs.write.pickle("cache_graph.pkl", result)

    wiz.response.status(200, result)

    # wiz.response.status(200, {'weight_means': weight_means, 'bmi_means': bmi_means, 'labels': labels})