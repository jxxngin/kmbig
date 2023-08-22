import season
import time
import datetime
import os
import urllib

orm = wiz.model("orm")

segment = wiz.request.match("/files/expert/<action>/<category>/<docID>/<expertID>/<dataID>/<path:path>")
action = segment.action
category = segment.category
docID = segment.docID
expertID = segment.expertID
dataID = segment.dataID

fs = wiz.model("fs").use(f"{category}/{dataID}/share/{docID}/expert/{expertID}")

if action == 'upload':
    file = wiz.request.file("upload")    
    if len(file.filename) == 0: 
        wiz.response.status(404)

    filepath = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_" + orm.random(8)
    fs.write.file(filepath, file)
    urlfilename = urllib.parse.quote(file.filename)
    wiz.response.json({"url": f'/files/expert/download/{category}/{docID}/{expertID}/{dataID}/{filepath}/{urlfilename}'})

elif action == 'download':
    segment = wiz.request.match("/files/expert/<action>/<category>/<docID>/<expertID>/<dataID>/<filepath>/<filename>")
    filepath = segment.filepath
    filename = segment.filename
    filename = urllib.parse.unquote(filename)

    if fs.isfile(filepath) == False:
        wiz.response.abort(404)
        
    filepath = fs.abspath(filepath)
    wiz.response.download(filepath, as_attachment=False, filename=filename)
