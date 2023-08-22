def load():
    category = wiz.request.query('category', True)
    db = wiz.model('orm').use('pages')
    row = db.get(pages=category, fields="id,pages,content")

    if row == None:
        wiz.response.status(201)

    wiz.response.status(200, row)

def save():
    info = wiz.request.query()

    storage = wiz.model("storage").use(f"page/{info['pages']}")
    filename = f"{info['pages']}.html"
    filepath = storage.abspath(filename)
    storage.write.text(filepath, info['content'])
    info['filepath'] = filepath
    
    db = wiz.model("orm").use("pages")
    db.update(info, pages=info['pages'])

    wiz.response.status(200, True)