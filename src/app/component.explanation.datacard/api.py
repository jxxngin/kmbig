import random

def load():
    category = wiz.request.query("category", True)
    dataDB = wiz.model("orm").use("dataset")
    # dataList = dataDB.rows(category=category, fields="id,title,category,department")
    dataList = dataDB.rows(fields="id,title,category,department")

    randomList = random.sample(dataList, 3)

    wiz.response.status(200, randomList)