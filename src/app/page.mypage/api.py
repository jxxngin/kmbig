import json

orm = wiz.model("orm")
db = orm.use("user")

def session():
    resp = dict()
    user_id = wiz.session.get("id")
    user = db.get(id=user_id)
    del user['password']
    
    wiz.response.status(200, user)

def update():
    user = json.loads(wiz.request.query("userinfo", True))
    del user['id']
    del user['created']
    del user['role']
    del user['email']
    user_id = wiz.session.get("id")
    db.update(user, id=user_id)
    wiz.response.status(200, True)

def change_password():
    current = wiz.request.query("current", True)
    data = wiz.request.query("data", True)
    user_id = wiz.session.get("id")
    user = db.get(id=user_id)

    if user['password'](current) == False:
        wiz.response.status(401, "비밀번호가 틀렸습니다")
    
    db.update(dict(password=data), id=user_id)

    wiz.response.status(200, True)