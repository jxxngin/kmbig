import os
import json
import shutil
import datetime

import zipfile
import tempfile

wiz.session = wiz.model("session").use()
user_id = wiz.session.get("id")
user_name = wiz.session.get("name")

def init():
    path = f"user/{user_id}"
    wiz.response.status(200, path)

def list(segment):
    path = wiz.request.query("path", True)

    storage = wiz.model("storage").use(path)
    BASEPATH = storage.abspath()

    if os.path.isdir(BASEPATH):
        files = os.listdir(BASEPATH)
        res = []

        # for name in files:
        #     fpath = os.path.join(path, name)
        #     ftype = 'file' if os.path.isfile(fpath) else 'folder'
        #     res.append(dict(name=name, path=fpath, type=ftype))

        for name in files:
            fpath = os.path.join(BASEPATH, name)
            if os.path.isdir(fpath):
                updated = os.path.getmtime(fpath)
                fpath = os.path.relpath(fpath, wiz.model("storage").use().abspath())
                updated = datetime.datetime.fromtimestamp(updated)
                res.append(dict(name=name, path=fpath, type='folder', updated=updated))
        res = sorted(res, key=lambda x: x['updated'], reverse=True)
        wiz.response.status(200, res)
     
    wiz.response.status(404, [])

def load():
    base = wiz.request.query("base", True)

    storage = wiz.model("storage").use(base)
    BASEPATH = storage.abspath()
    files = storage.ls()

    for i in range(len(files)):
        path = os.path.join(BASEPATH, files[i])
        info = dict()
        info['name'] = files[i]
        info['path'] = path
        info['type'] = 'folder'
        # info['size'] = os.path.getsize(path)
        info['updated'] = datetime.datetime.fromtimestamp(os.path.getmtime(path)).isoformat()

        if storage.isfile(path):
            info['type'] = 'file'
            info['size'] = os.path.getsize(path)

        files[i] = info
    
    files = sorted(files, key=lambda x: (x['type'] != 'file', x['updated']), reverse=True)

    for i in range(len(files)):
        files[i]['updated'] = files[i]['updated'][:10]
         
    wiz.response.status(200, {
        "user" : user_name,
        "files" : files
    })

def remove():
    base = wiz.request.query("base", True)

    remove_file = wiz.request.query("file", "{}")
    remove_file = json.loads(remove_file)

    storage = wiz.model("storage").use(base)
    BASEPATH = storage.abspath()
    path = os.path.join(BASEPATH, remove_file['name'])

    if os.path.isfile(path):
        os.remove(path)
        wiz.response.status(200)

    elif os.path.isdir(path):
        shutil.rmtree(path)
        wiz.response.status(200)

    else:
        wiz.response.status(400)

def create():
    base = wiz.request.query("base", True)
    dir_name = wiz.request.query("dirName", True)

    storage = wiz.model("storage").use(base)
    BASEPATH = storage.abspath()
    path = os.path.join(BASEPATH, dir_name)

    if not os.path.exists(path):
        os.makedirs(path)
        wiz.response.status(200)
    else:
        wiz.response.status(201)

def upload():
    files = wiz.request.files()
    filepath = json.loads(wiz.request.query("filepath", True))
    storagepath = wiz.config("config").STORAGE_PATH + "/"

    for index, item in enumerate(files):
        path = os.path.join(storagepath, filepath[index])
        fs = season.util.os.FileSystem(path)
        fs.write.file(item.filename, item)

def rename():
    base = wiz.request.query("base", True)
    name = wiz.request.query("name", True)
    old_path = wiz.request.query("path", True)

    storage = wiz.model("storage").use(base)
    BASEPATH = storage.abspath()
    new_path = os.path.join(BASEPATH, name)

    if os.path.exists(old_path):
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            wiz.response.status(200)
        else:
            wiz.response.status(202)
    else:
        wiz.response.status(201)

def download():
    path = wiz.request.query("path")
    storage = wiz.model("storage").use(path)
    BASEPATH = storage.abspath()

    filename = wiz.request.query("name", True)
    filepath = os.path.join(BASEPATH, filename)

    if os.path.isdir(filepath):
        filename += ".zip"
        zippath = os.path.join(tempfile.gettempdir(), filename)
        
        try:
            os.remove(zippath)
        except:
            pass
        
        os.makedirs(os.path.dirname(zippath), exist_ok=True)
        zipdata = zipfile.ZipFile(zippath, 'w')
        for folder, _, files in os.walk(filepath):
            for file in files:
                zipdata.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), filepath), compress_type=zipfile.ZIP_DEFLATED)
        zipdata.close()
        filepath = zippath

    wiz.response.download(filepath, as_attachment=True, filename=filename)

def macro():
    filepath = wiz.request.query("filepath", True)
    filename = filepath.split("/")[-1]
    fname, fileExtension = os.path.splitext(filename)

    where = {
        'filetype': fileExtension[1:],
    }
    like = 'filetype'
    fields = "num,id,title,namespace"
    macroDB = wiz.model("orm").use("macro")
    macroRows = macroDB.rows(fields=fields, like=like, **where)

    wiz.response.status(200, macroRows)