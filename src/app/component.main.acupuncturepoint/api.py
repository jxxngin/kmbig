orm = wiz.model("orm")
point_db = orm.use("acupuncture_point")

def load():
    rows = point_db.rows(fields="title", orderby="id", order="ASC")
    res = list(map(lambda x: x['title'], rows))
    col1 = res[:13]
    col2 = res[13:]
    wiz.response.status(200, {
        "col1": col1,
        "col2": col2,
    })

def path():
    point = wiz.request.query("point", "")
    row = point_db.get(title=point)

    img_path = dict()

    if row['cnt'] == 1:
        img_path[0] = "/assets/images/main/acupuncture_point/" + row['img'] + ".svg"
    elif row['cnt'] > 1:
        for i in range(1, row['cnt']+1):
            img_path[i-1] = "/assets/images/main/acupuncture_point/" + row['img'] + "-" + str(i) + ".svg"
    elif row['cnt'] == 0:
        img_path[0] = ""
    else:
        wiz.response.status(401)
    
    wiz.response.status(200, img_path)