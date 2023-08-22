import season
import time
import datetime
import os
import urllib

orm = wiz.model("orm")

segment = wiz.request.match("/files/data/<action>/<category>/<dataset_id>/<path:path>")
action = segment.action
dataset_id = segment.dataset_id
category = segment.category

fs = wiz.model("fs").use(f"{category}/{dataset_id}/image")
user_id = wiz.session.get("id", None)

if action == 'upload':
    file = wiz.request.file("upload")    
    if len(file.filename) == 0: 
        wiz.response.status(404)

    filepath = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_" + orm.random(8)
    fs.write.file(filepath, file)
    urlfilename = urllib.parse.quote(file.filename)
    wiz.response.json({"url": f'/files/data/download/{category}/{dataset_id}/{filepath}/{urlfilename}'})

elif action == 'download':
    segment = wiz.request.match("/files/data/<action>/<category>/<dataset_id>/<filepath>/<filename>")
    filepath = segment.filepath
    filename = segment.filename
    filename = urllib.parse.unquote(filename)

    if fs.isfile(filepath) == False:
        wiz.response.abort(404)
        
    filepath = fs.abspath(filepath)
    wiz.response.download(filepath, as_attachment=False, filename=filename)
