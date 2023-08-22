import os
import pandas as pd
import json
import simplejson
import math
from openpyxl import load_workbook
from collections import Counter

def fileInfo():
    dataset_id = wiz.request.query('id', True)
    category = wiz.request.query('category', True)

    file_db = wiz.model('orm').use('files')
    file_info = file_db.get(dataset_id=dataset_id, fields='name,filepath,rows')
    name = file_info['name']
    filepath = file_info['filepath']

    filename, fileExtension = os.path.splitext(name)
    if fileExtension == '.xlsx':
        df = pd.read_excel(filepath, engine='openpyxl')
    elif fileExtension == '.csv':
        df = pd.read_csv(filepath, encoding='utf8')
    # df = pd.read_excel('/var/www/kmbig_admin/storage/files/device/NQkDpJRs556TdhQNhOt27rTq73hIwi8H/export_tnmebloodpressure_(혈압)_2022.xlsx', engine='openpyxl').head(10)
    
    if(dataset_id == 'Giesy5Us4z6EekMlx12HcAfalV1JYasA'):
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
        
        total = sum(value)
        value = [round((val / total) * 100, 2) for val in value]
    
    if(dataset_id == 'k1pkjQJFhmmC9sSXCt23g4SAvKYtVDp1'):
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

    if(dataset_id == 'yd5m3OpaRuAbm2dfRyh7ks2LT4e5vqsZ'):
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

    wiz.response.status(200, result)