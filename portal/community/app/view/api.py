orm = wiz.model("orm")
board_db = orm.use("board")
user_db = orm.use("user")
wiz.session = wiz.model("session").use()

def load():
    id = wiz.request.query("id", True)
    row = board_db.get(id=id)
    
    user_id = row['user_id']
    user = user_db.get(id=user_id, fields="id,name")

    login = dict()
    login['id'] = wiz.session.get('id')
    login['role'] = wiz.session.get('role')
    
    wiz.response.status(200, {
        "view": row,
        "user": user,
        "login": login,
    })