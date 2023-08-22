orm = wiz.model("orm")
dataset_db = orm.use("dataset")
files_db = orm.use("files")

def load_card():
    dataset = dataset_db.count()
    download = 0
    files = files_db.count()
    size = 0

    row = dataset_db.rows(fields="download_count")
    res = list(map(lambda x: x["download_count"], row))

    for i in range(len(res)):
        download += res[i]

    row = files_db.rows(fields="size")
    res = list(map(lambda x: x["size"], row))

    for i in range(len(res)):
        size += res[i]

    data = dict()
    
    if size < 1e+3:
        size = round(size, 1)
        data['type'] = 'B'
    elif size < 1e+6:
        size /= 1e+3
        size = round(size, 1)
        data['type'] = 'KB'
    elif size < 1e+9:
        size /= 1e+6
        size = round(size, 1)
        data['type'] = 'MB'
    else:
        size /= 1e+9
        size = round(size, 1)
        data['type'] = 'GB'
    
    data['dataset'] = dataset
    data['download'] = download
    data['files'] = files
    data['size'] = size

    wiz.response.status(200, data)