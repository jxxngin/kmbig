def load():
    dashboard_category = wiz.request.query("id", True)
    dashboard_db = wiz.model('orm').use('dashboard')
    dashboard_row = dashboard_db.get(title=dashboard_category, fields="id,title,category,content")

    db = wiz.model('orm').use('dataset')
    rows = db.rows(fields="id,title",orderby="title",category=dashboard_row["title"])

    fs = wiz.model("fs").use(f"dashboard/medicine/manage")
    fileList = fs.ls()
    fileInfo = []
    for file in fileList:
        fileDic = dict()
        fileDic["filename"] = file
        if file == "medicinal_material.xlsx":
            fileDic["title"] = "약재 재료 목록"
            fileDic["row"] = "635"
        elif file == "medicinal_compound.xlsx":
            fileDic["title"] = "약용-화합물"
            fileDic["row"] = "100,076"
        elif file == "chemical_property.xlsx":
            fileDic["title"] = "화학적 특성"
            fileDic["row"] = "21,580"
        elif file == "chemical_protein.xlsx":
            fileDic["title"] = "화합물-단백질 연결"
            fileDic["row"] = "419,609"
        elif file == "protein_disease.xlsx":
            fileDic["title"] = "단백질-질병 연결"
            fileDic["row"] = "842,233"
        elif file == "prescription.xlsx":
            fileDic["title"] = "처방"
            fileDic["row"] = "40,588"
        fileInfo.append(fileDic)
    
    wiz.response.status(200, {'dashboard_row':dashboard_row, 'dataset_row':rows, 'fileInfo':fileInfo})

def download():
    filename = wiz.request.query("file", True)
    fs = wiz.model("fs").use(f"dashboard/medicine/manage")
    filepath = fs.abspath(filename)
    wiz.response.download(filepath, as_attachment=True, filename=filename)