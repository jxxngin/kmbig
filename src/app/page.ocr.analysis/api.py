import io
import os
import json
import shutil
import datetime
import pandas as pd

import fitz
from PIL import Image

orm = wiz.model("orm")
infoDB = orm.use("ocr_info")
dataDB = orm.use("ocr_data")

def load():
    id = wiz.request.query("id", True)

    info = infoDB.get(id=id)
    data = dataDB.rows(ocr_id=id, orderby="question_id,question_sub")

    wiz.response.status(200, {
        "info": info,
        "data": data,
    })

def upload():
    files = wiz.request.files()[0]
    filepath = json.loads(wiz.request.query("filepath", True))
    filename = json.loads(wiz.request.query("filename", True))
    storagepath = wiz.config("config").STORAGE_PATH + "/"

    path = os.path.join(storagepath, filepath)

    if not os.path.exists(path):
        os.makedirs(path)
    
    fs = season.util.os.FileSystem(path)
    fs.write.file(filename, files)

def pdf():
    id = wiz.request.query("id", True)
    name = wiz.request.query("name", True)

    storagepath = wiz.config("config").STORAGE_PATH + "/"
    path = storagepath + "ocr/" + id + "/analysis/" + name

    doc = fitz.open(path)
    images = []

    for i in range(len(doc)):
        page = doc.load_page(i)
        pix = page.get_pixmap()

        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        imagePath = f"{os.path.splitext(path)[0]}_{i+1}.png"
        image.save(imagePath)
        images.append(imagePath)
    
    wiz.response.status(200, images)

def download():
    path = wiz.request.query("path", True)
    storage = wiz.model("storage").use(path)
    BASEPATH = storage.abspath()

    filename = wiz.request.query("name", True)
    filepath = os.path.join(BASEPATH, filename)

    wiz.response.download(filepath, as_attachment=False, filename=filename)

def excel():
    id = wiz.request.query("id", True)
    result = wiz.request.query("result", True)
    result = json.loads(result)
    name = wiz.request.query("name", True)
    name = json.loads(name)

    # question
    df_question = pd.DataFrame()
    q_rows = dataDB.rows(ocr_id=id, orderby="question_id,question_sub", fields="question_id,question_sub,question_name,result")
    
    for i, res in enumerate(q_rows):
        df_question = df_question.append({
            'question_id': res['question_id'],
            'question_sub': res['question_sub'],
            'question_name': res['question_name'],
            'result': res['result']
        }, ignore_index=True)

    # answer
    df_answer = pd.DataFrame()

    for i, res in enumerate(result):
        for item in res:
            true_indices = [str(j + 1) for j, ans in enumerate(item['answer']) if ans]
            if true_indices:
                df_answer = df_answer.append({
                    'name': name[i],
                    'question_id': item['question_id'],
                    'question_sub': item['question_sub'], 
                    'answer': ','.join(true_indices)
                }, ignore_index=True)

    df_answer['question'] = df_answer['question_id'].astype(str)
    df_answer.loc[df_answer['question_sub'] != '', 'question'] += "-" + df_answer['question_sub'].astype(str)

    df_answer = df_answer.pivot_table(index=['name'], columns='question', values='answer', aggfunc='first').reset_index()

    cols = df_answer.columns.tolist()
    sorted_cols = sorted([col for col in cols if '-' in col or col.isdigit()], key=lambda x: (int(x.split('-')[0]), x))
    remaining_cols = [col for col in cols if col not in sorted_cols]
    df_answer = df_answer[remaining_cols + sorted_cols]


    # file setting
    storagepath = wiz.config("config").STORAGE_PATH + "/"
    path = storagepath + "ocr/" + id + "/analysis"

    info = infoDB.get(id=id)
    date = datetime.datetime.now().strftime('%y%m%d')

    filename = info['name'] + "_" + date + "_" + str(len(name)) + ".xlsx"
    filepath = os.path.join(path, filename)

    with pd.ExcelWriter(filepath) as writer:
        df_question.to_excel(writer, sheet_name="code", index=False)
        df_answer.to_excel(writer, sheet_name="data", index=False)

    wiz.response.status(200, {
        "filename": filename,
        "filepath": path
    })

def finish():
    id = wiz.request.query("id", True)
    
    storagepath = wiz.config("config").STORAGE_PATH + "/"
    path = storagepath + "ocr/" + id + "/analysis"
    
    shutil.rmtree(path)
    wiz.response.status(200)