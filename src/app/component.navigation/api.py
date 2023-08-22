def user():
    wiz.session = wiz.model("session").use()
    user_name = wiz.session.get('name')
    user_role = wiz.session.get('role')
    wiz.response.status(200, {"name":user_name, "role":user_role})

def load():
    dashDB = wiz.model("orm").use("dashboard")
    dashRow = dashDB.rows(fields="title,category")
    wiz.response.status(200, dashRow)

def noti():
    orm = wiz.model("orm")
    notification = orm.use("notification")
    wiz.session = wiz.model("session").use()

    id = wiz.session.get("id")
    rows = notification.rows(user=id)

    for i in range(len(rows)):
        if rows[i]['show'] == 0:
            wiz.response.status(200, True)
    
    wiz.response.status(200, False)
