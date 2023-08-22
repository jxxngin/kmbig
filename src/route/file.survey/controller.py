import os

segment = wiz.request.match("/file/survey/<surveyID>/<path:path>")
surveyID = segment.surveyID
filepath = segment.path

fs = wiz.model("fs").use(f"survey")
abspath = fs.abspath(filepath)

wiz.response.download(abspath, as_attachment=True)