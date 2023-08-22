def load():
    ocrDB = wiz.model("orm").use("ocr_info")
    rows = ocrDB.rows(order="ASC", orderby="created")
    
    wiz.response.status(200, rows)