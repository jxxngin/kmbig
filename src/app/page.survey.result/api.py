import pandas as pd
import numpy as np
import os
import re
import json
import copy

surveyDB = wiz.model("orm").use("survey")

def load():
    surveyID = wiz.request.query("id", True)
    fs = wiz.model("fs").use(f"survey/{surveyID}")
    surveyInfo = surveyDB.get(id=surveyID)
    questionFile = ""
    if surveyInfo["question_file"] is not None:
        questionFile, fileExtension = os.path.splitext(surveyInfo["question_file"])
    filename = surveyInfo["answer_file"]
    filepath = fs.abspath(filename)

    hospitalIDs = json.loads(wiz.request.query("hospitalIDs", True))
    yearIDs = json.loads(wiz.request.query("yearIDs", True))
    if (len(hospitalIDs)==0 or len(yearIDs)==0):
        wiz.response.status(204, False)

    hospitalIDs.sort()
    yearIDs.sort()
    containh = "|".join(hospitalIDs)
    containy = "|".join(yearIDs)

    hylist = hospitalIDs + yearIDs
    hylist.sort()
    cached = "_".join(hylist)

    # cache
    if fs.exists(f"cache_{cached}.pkl"):
        end = fs.read.pickle(f"cache_{cached}.pkl")
        wiz.response.status(200, end)

    try:
        # 파일 열기
        codeBookDF = pd.read_excel(filepath, sheet_name="코드북", engine='openpyxl')
        qDF = codeBookDF[["변경사항", "TABLENAME", "VARSTD", "Contents 1", "Contents 2", "비고"]]
        aDF = pd.read_excel(filepath, sheet_name="data", engine='openpyxl')

        # question에서 넘버링만 포함된 컬럼만 추출 & (?)년도 삭제된 컬럼 제거
        columnsDel = ['WAISTCIRCD', 'BMICD', 'VALTCD', 'VARTCD', 'BPCD', 'WATERCUPSIZE', 'SLEEPTIME_1200_1230', 'SLEEPTIME_1230_1300', 'SLEEPTIME_1300_1330', 'SLEEPTIME_1330_1400', 'SLEEPTIME_1400_1430', 'SLEEPTIME_1430_1500', 'SLEEPTIME_1500_1530', 'SLEEPTIME_1530_1600', 'SLEEPTIME_1600_1630', 'SLEEPTIME_1630_1700', 'SLEEPTIME_1700_1730', 'SLEEPTIME_1730_1800', 'SLEEPTIME_1800_1830', 'SLEEPTIME_1830_1900', 'SLEEPTIME_1900_1930', 'SLEEPTIME_1930_2000', 'SLEEPTIME_2000_2030', 'SLEEPTIME_2030_2100', 'SLEEPTIME_2100_2130', 'SLEEPTIME_2130_2200', 'SLEEPTIME_2200_2230', 'SLEEPTIME_2230_2300', 'SLEEPTIME_2300_2330', 'SLEEPTIME_2330_2400', 'SLEEPTIME_0000_0030', 'SLEEPTIME_0030_0100', 'SLEEPTIME_0100_0130', 'SLEEPTIME_0130_0200', 'SLEEPTIME_0200_0230', 'SLEEPTIME_0230_0300', 'SLEEPTIME_0300_0330', 'SLEEPTIME_0330_0400', 'SLEEPTIME_0400_0430', 'SLEEPTIME_0430_0500', 'SLEEPTIME_0500_0530', 'SLEEPTIME_0530_0600', 'SLEEPTIME_0600_0630', 'SLEEPTIME_0630_0700', 'SLEEPTIME_0700_0730', 'SLEEPTIME_0730_0800', 'SLEEPTIME_0800_0830', 'SLEEPTIME_0830_0900', 'SLEEPTIME_0900_0930', 'SLEEPTIME_0930_1000', 'SLEEPTIME_1000_1030', 'SLEEPTIME_1030_1100', 'SLEEPTIME_1100_1130', 'SLEEPTIME_1130_1200', 'AE_YN']
        columnsStr = '|'.join(columnsDel)

        qDF = qDF[qDF["비고"].str.contains("①|01|1 2 3", na=False)]
        qDF = qDF[~qDF["변경사항"].str.contains("삭제", na=False)]

        columnsAll = qDF["VARSTD"].values.tolist()

        # question에서 Contents 1과 Contents 2 합치기
        def combine_2rd_columns(col_1, col_2):
            result = col_1
            if not pd.isna(col_2):
                result += " - " + str(col_2)
            return result
        qDF["Contents"] = qDF.apply(lambda x: combine_2rd_columns(x['Contents 1'], x['Contents 2']), axis=1)
        qDF = qDF.drop(['변경사항', 'Contents 1', 'Contents 2'], axis=1)

        # qustion에서 답변 넘버링 추출
        qDF["비고"] = qDF["비고"].str.split("①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩|⑪|⑫|\n|0: |01: |02: |03: |04: |05: |06: |07: |08: |Y: |N |0 ")

        sample = qDF["비고"].values.tolist()
        for i in range(len(sample)):
            if sample[i][0] == "":
                sample[i] = [n for n in sample[i] if n]
                sample[i].insert(0, "NONE")
            elif "0" in sample[i][0]:
                sample[i][0] = sample[i][0][2:]
                sample[i] = [n for n in sample[i] if n]
            elif len(sample[i]) == 1:
                sample[i] = list(re.sub(r'[^0-9]', '', sample[i][0]))
            else:
                sample[i] = [i for i in sample[i] if i not in {" "}]
                sample[i].insert(1, "보통")
                sample[i].insert(0, "NONE")

        qDF["비고"] = sample
        qDF = qDF.reset_index().drop(['index'], axis=1)

        # 년도별 건수
        aDF_20 = aDF[aDF["USUBJID"].str.contains("20-", na=False)]
        aDF_21 = aDF[aDF["USUBJID"].str.contains("21-", na=False)]
        aDF_22 = aDF[aDF["USUBJID"].str.contains("22-", na=False)]
        
        # 병원별 건수
        aDF_GC = aDF[aDF["USUBJID"].str.contains("GC", na=False)]
        aDF_PS = aDF[aDF["USUBJID"].str.contains("PS", na=False)]
        aDF_DS = aDF[aDF["USUBJID"].str.contains("DS", na=False)]
        aDF_DG = aDF[aDF["USUBJID"].str.contains("DG", na=False)]
        aDF_DJ = aDF[aDF["USUBJID"].str.contains("DJ", na=False)]

        # 병원별 & 년도별 뽑기 -> 병원끼리 or 조건, 년도끼리 or 조건, 병원/년도 and 조건
        # aDF = aDF[aDF["USUBJID"].str.contains(contain, na=False)]
        # aDF = aDF.drop(['USUBJID'], axis=1) 
        aDFh = copy.deepcopy(aDF)
        aDFy = copy.deepcopy(aDF)
        aDFh2 = aDFh[aDFh["USUBJID"].str.contains(containh, na=False)]
        aDFy2 = aDFy[aDFy["USUBJID"].str.contains(containy, na=False)]
        aDF = pd.merge(aDFh2, aDFy2, how='inner', indicator=True)
        same_rows = aDF[aDF['_merge'] == 'both']
        aDF = same_rows.drop(columns=['_merge', "USUBJID"])
        aDFLen = len(aDF)

    except Exception as e:
        print(e)
        wiz.response.status(500, e)
        
    # 데이터가 없을 경우,
    if aDFLen == 0:
        wiz.response.status(204, False)
    
    try:
        # answer에서 숫자가 아닌 것들 replace
        answer = aDF[columnsAll]
        answer = answer.replace({
            "Y":1, "N":2, "M":1, "F":2, 
            "20-29":1, "30-39":2, "40-49":3, "50-59":4, "60+":5, 
            "LH":1, "RH":2, "BH":3, 
            "MP":1, "PJ":2, "OW":3, "SP":4, "SL":5, "FF":6, "TS":7, "MO":8, "SW":9, "CS":10, "HW":11, "ETC":12,
            "SG":1, "MG":2, "BM":3, "DV":4, 
            "정상":1, "주의":2, "저비중":3, "고비중":4, "음성":1,
            "+":1, "-":2})
        didtjd3 = ["URGLUCNR", "KETONESNR", "OCCBLDNR", "PHNR", "URPROTNR", "NITRITENR", "URWBCNR"]
        for item in didtjd3:
            answer[item] = answer[item].replace({"양성":3})
        answer["UROBILNR"] = answer["UROBILNR"].replace({"양성":2})
        answer["URBILINR"] = answer["URBILINR"].replace({"양성":2})
        aDFfill = answer.fillna(100)

        # question에 answer 결과 리스트 DATA 열에 추가
        qDF=qDF.assign(DATA=np.nan)
        alll = []
        for i in range(len(qDF)):
            summ = []
            example = qDF.loc[i]["비고"]
            answers = aDFfill[qDF.loc[i]["VARSTD"]].values.tolist()
            for j in range(len(example)):
                summ.append(answers.count(j))
            alll.append(summ)
        qDF["DATA"] = alll

        # [{'groupID': 'SC12.증례기록정보', 'content': ['성별 (Sex)', '연령대'], 'note': [['NONE', ' 남자(M) ', ' 여자(F)'], ['NONE', ' 20-29 ', ' 30-39 ', ' 40-49 ', ' 50-59', ' 60+']], 'data': [[0, 27, 73], [0, 6, 13, 28, 21, 32]]}}
        groupIDs = []
        result = []
        cache = dict()
        for g in range(len(qDF)):
            item = qDF.iloc[g]
            groupID = item["TABLENAME"]
            question = item["Contents"]
            example = item["비고"]
            answer = item["DATA"]

            if groupID in cache:
                continue
            groupIDs.append(groupID)
            partDF = qDF[qDF["TABLENAME"]==groupID]
            conCol = partDF["Contents"].values.tolist()
            noteCol = partDF["비고"].values.tolist()
            dataCol = partDF["DATA"].values.tolist()
            cache[groupID] = dict(groupID=groupID, content=conCol, note=noteCol, data=dataCol)
            result.append(cache[groupID])

        end = dict()
        end["preview"] = questionFile
        end["result"] = result
        end["groups"] = groupIDs
        end["count"] = [len(aDF_GC), len(aDF_PS), len(aDF_DS), len(aDF_DG), len(aDF_DJ)]
        end["count2"] = [len(aDF_20), len(aDF_21), len(aDF_22)]
        fs.write.pickle(f"cache_{cached}.pkl", end)

    except Exception as e:
        print(e)
        wiz.response.status(500, e)

    wiz.response.status(200, end)

def download():
    surveyID = wiz.request.query("id")
    storage = wiz.model("storage").use("survey")
    BASEPATH = storage.abspath()

    filename = wiz.request.query("title", True) + ".xlsx"
    filepath = os.path.join(BASEPATH, surveyID, filename)

    wiz.response.download(filepath, as_attachment=True, filename=filename)

def pdf():
    surveyID = wiz.request.query("id", True)
    filename = wiz.request.query("file", True)
    fs = wiz.model("fs").use(f"survey/{surveyID}")
    filepath = fs.abspath(f"{filename}.pdf")
    wiz.response.download(filepath, as_attachment=False)