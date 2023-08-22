import json
import pandas as pd
import numpy as np
import os

def result():
    dataID = wiz.request.query("id", True)
    filtered = wiz.request.query("filter", True)
    filtered = json.loads(filtered)

    # 필터 값 추출
    period = [key for key, value in filtered["period"].items() if value is True]
    age = [key for key, value in filtered["age"].items() if value is True]
    sex = [key for key, value in filtered["sex"].items() if value is True]
    sasang = [key for key, value in filtered["sasang"].items() if value is True]
    height1 = filtered['height1']
    height2 = filtered['height2'] 
    weight1 = filtered['weight1']
    weight2 = filtered['weight2']
    periods = '_'.join(sorted(period))
    ages = '_'.join(sorted(age))
    sexs = '_'.join(sorted(sex))
    sasangs = '_'.join(sorted(sasang))
    total = f"{periods}-{ages}-{sexs}-{sasangs}-{height1}_{height2}-{weight1}_{weight2}.pkl"

    fs = wiz.model("fs").use(f"dataset/{dataID}/cache/inquire")
    if fs.exists(total):
        length = fs.read.pickle(total)
        wiz.response.status(200, length)

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
    
    # # 필터 값 추출
    # period = [key for key, value in filtered["period"].items() if value is True]
    # age = [key for key, value in filtered["age"].items() if value is True]
    # sex = [key for key, value in filtered["sex"].items() if value is True]
    # sasang = [key for key, value in filtered["sasang"].items() if value is True]
    # height1 = filtered['height1']
    # height2 = filtered['height2'] 
    # weight1 = filtered['weight1']
    # weight2 = filtered['weight2'] 

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
    length = len(df_without_nan)
    fs.write.pickle(total, length)
        
    wiz.response.status(200, length)