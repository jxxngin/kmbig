import os

def load():
    id = wiz.request.query("id", True)
    db = wiz.model("orm").use("dataset")
    row = db.get(id=id, fields="content,category")

    fileDB = wiz.model("orm").use("files")
    fileInfo = fileDB.rows(dataset_id=id, fields="year,rows")

    result = dict()
    result['dataInfo'] = row
    result['fileInfo'] = fileInfo

    # dataPath = f"files/{id}/manage/sop"
    dataPath = f"dataset/{id}/manage/sop"
    storage = wiz.model("storage").use(dataPath)
    BASEPATH = storage.abspath()

    if storage.isdir(BASEPATH):
        files = os.listdir(BASEPATH)
        files.sort(key=lambda x: int(x) if x.isdigit() else x, reverse=True)

        if len(files) == 0:
            wiz.response.status(201, result)

        res = []
        for name in files:
            fpath = os.path.join(BASEPATH, name)
            res.append(dict(name=name, path=fpath))
        result['fileList'] = res

    wiz.response.status(200, result)

def download():
    filepath = wiz.request.query("path", True)
    filename = wiz.request.query("name", True)

    wiz.response.download(filepath, as_attachment=True, filename=filename)