import io
import os
import datetime
import json
import shutil

import fitz
from PIL import Image
from ast import literal_eval

infoDB = wiz.model("orm").use("ocr_info")
dataDB = wiz.model("orm").use("ocr_data")

def init():
    name = wiz.request.query("name", True)

    info = dict()
    info['id'] = wiz.model('orm').random(length=8)
    info['name'] = name
    info['created'] = datetime.datetime.now()

    infoDB.insert(info)

    wiz.response.status(200, info['id'])


def load():
    id = wiz.request.query("id", True)

    info = infoDB.get(id=id)
    data = dataDB.rows(ocr_id=id, orderby="question_id,question_sub")
    
    wiz.response.status(200, { 
        "info": info,
        "data": data 
    })

def request():
    ocrID = wiz.request.query("id", True)
    info = wiz.request.query("info", True)
    info = json.loads(info)
    data = wiz.request.query("list", True)
    data = json.loads(data)

    infoDB.update(info, id=info['id'])
    
    for item in data:
        if "setting" in item:
            del item["setting"]
        
        if "id" not in item:
            item['ocr_id'] = ocrID
            item['created'] = datetime.datetime.now()
            dataDB.insert(item)
        else:
            dataDB.update(item, id=item['id'])

    wiz.response.status(200)

def remove():
    ocrID = wiz.request.query("id", True)

    infoDB.delete(id=ocrID)
    dataDB.delete(ocr_id=ocrID)

    storagepath = wiz.config("config").STORAGE_PATH + "/"
    path = storagepath + "ocr/" + ocrID;
    
    shutil.rmtree(path)
    wiz.response.status(200)

def deleteQ():
    qID = wiz.request.query("qID", True)
    dataDB.delete(id=qID)

    wiz.response.status(200)

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
    path = storagepath + "ocr/" + id + "/pdf/" + name;

    doc = fitz.open(path)
    images = []

    for i in range(len(doc)):
        page = doc.load_page(i)
        pix = page.get_pixmap()

        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        imagePath = f"{os.path.splitext(path)[0]}_{i+1}.png"
        image.save(imagePath)
        images.append(imagePath)
    
    info = dict()
    info['file'] = name
    info['images'] = json.dumps(images)
    infoDB.update(info, id=id)
    
    wiz.response.status(200, {
        "images": images,
        "lastPage": len(doc)
    })

def download():
    path = wiz.request.query("path")
    storage = wiz.model("storage").use(path)
    BASEPATH = storage.abspath()

    filename = wiz.request.query("name", True)
    filepath = os.path.join(BASEPATH, filename)

    wiz.response.download(filepath, as_attachment=False, filename=filename)