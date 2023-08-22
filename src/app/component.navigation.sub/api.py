def user():
    wiz.session = wiz.model("session").use()
    user_name = wiz.session.get('name')
    user_role = wiz.session.get('role')
    wiz.response.status(200, {"name":user_name, "role":user_role})

def load():
    dashDB = wiz.model("orm").use("dashboard")
    dashRow = dashDB.rows(fields="title,category")
    wiz.response.status(200, dashRow)