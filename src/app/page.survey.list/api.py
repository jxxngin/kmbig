def load():
    surveyDB = wiz.model("orm").use("survey")
    rows = surveyDB.rows(order="ASC", orderby="created")
    
    wiz.response.status(200, rows)