import datetime
import json
from ast import literal_eval
import os

surveyDB = wiz.model("orm").use("survey")

def load():
    surveyID = wiz.request.query("id", True)

    # 설문 추가 기능
    if surveyID == "new":
        surveyID = wiz.model('orm').random(length=16)
        new = dict()
        new['id'] = surveyID
        new['title'] = "새로운 설문"
        new['created'] = datetime.datetime.now()
        # surveyDB.insert(new)
        wiz.response.status(200, new)

    surveyInfo = surveyDB.get(id=surveyID)

    wiz.response.status(200, surveyInfo)

def request():
    surveyInfo = json.loads(wiz.request.query('info',True))
    # surveyDB.update(surveyInfo, id=surveyInfo["id"])
    # surveyDB.insert(surveyInfo)
    surveyDB.upsert(surveyInfo)

    fs = wiz.model("fs").use(f"survey/{surveyInfo['id']}")
    ls = fs.list()
    for item in ls:
        if "cache" in item:
            fs.delete(item)

    wiz.response.status(200, True)

def delete():
    surveyID = wiz.request.query("id", True)
    surveyDB.delete(id=surveyID)

    fs = wiz.model("fs").use(f"survey")
    fs.remove(surveyID)
    wiz.response.status(200, True)

def upload():
    files = wiz.request.files()
    data = json.loads(wiz.request.query('data',True))["data"]

    res = []
    for item in files:
        fs = wiz.model("fs").use(f"survey/{data['id']}")
        fs.write.file(item.filename, item)
        abspath = fs.abspath()
        filepath = os.path.join(abspath, item.filename)
        res.append(dict(filename=item.filename, url=f"/file/survey/{data['id']}/{item.filename}"))
        
        data["filepath"] = filepath

    wiz.response.status(200, {"res":res, "filepath":filepath})

def removeFile():
    surveyID = wiz.request.query("surveyID", True)
    filename = wiz.request.query("filename", True)

    fs = wiz.model("fs").use(f"survey/{surveyID}")
    fs.remove(filename)

    wiz.response.status(200)

def download():
    surveyID = wiz.request.query("id", True)
    filename = wiz.request.query("name", True)
    fs = wiz.model("fs").use(f"survey/{surveyID}")
    filepath = fs.abspath(filename)

    wiz.response.download(filepath, as_attachment=True, filename=filename)