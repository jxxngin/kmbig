import math

orm = wiz.model("orm")
board_db = orm.use("board")
comment_db = orm.use("comment")
user_db = orm.use("user")
wiz.session = wiz.model("session").use()

def load():
    page = int(wiz.request.query("page", 1))
    category = wiz.request.query("category", True)
    dump = 14
    where = dict(
        orderby="created",
        order="DESC",
        page=page,
        category=category,
        dump=dump,
    )
    rows = board_db.rows(**where)
    lastpage = math.ceil(board_db.count(**where) / dump)

    for i in range(len(rows)):
        rows[i]['comment'] = comment_db.count(board_id=rows[i]['id'])
        rows[i]['user'] = user_db.get(id=rows[i]['user_id'], fields="id,name")
    
    login = wiz.session.get('id')

    wiz.response.status(200, {
        "lastpage": lastpage,
        "list": rows,
        "login": login,
    })