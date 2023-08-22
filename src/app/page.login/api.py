db = wiz.model("orm").use("user")

def login():
    email = wiz.request.query("email", True)
    password = wiz.request.query("password", True)
    user = db.get(email=email)
    if user is None:
        wiz.response.status(402, "이메일을 확인해주세요")
    if user['password'](password) == False:
        wiz.response.status(403, "비밀번호를 확인해주세요")
    del user['password']
    wiz.session.set(**user)
    wiz.response.status(200, True)