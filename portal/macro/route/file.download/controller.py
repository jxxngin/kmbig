import season
import time
import datetime
import os
import urllib

orm = wiz.model("orm")

segment = wiz.request.match("/file/<action>/<path:path>")
action = segment.action
path = segment.path

wiz.session = wiz.model("session").use()
userID = wiz.session.get("id", None)
fs = wiz.model("fs").use(f"user/{userID}/분석결과")

if action == 'download':
    filename = path.split("/")[-1]
    filepath = fs.abspath(filename)
    print("filepath : ", filepath)
    print("filename : ", filename)
    wiz.response.download(filepath, as_attachment=False, filename=filename)
