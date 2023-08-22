import datetime

orm = wiz.model("orm")
boarddb = orm.use("board")
wiz.session = wiz.model("session").use()

def load(wiz):
    post_id = wiz.request.query('id', True)
    data = boarddb.get(id=post_id)
    login = wiz.session.get()

    wiz.response.status(200, {
        "post": data,
        "login": login,
    })

def create(wiz):
    title = wiz.request.query('title', True)
    priority = wiz.request.query('priority', 0)
    content = wiz.request.query('content', True)
    category = wiz.request.query('category', True)

    post = dict()
    post['title'] = title
    post['category'] = category
    post['user_id'] = wiz.session.get('id')
    post['priority'] = priority
    post['content'] = content
    post['created'] = datetime.datetime.now()

    boarddb.insert(post)

    wiz.response.status(200, True)

def update(wiz):
    post_id = wiz.request.query('id', True)
    title = wiz.request.query('title', True)
    priority = wiz.request.query('priority', 0)
    content = wiz.request.query('content', True)

    post = dict()
    post['id'] = post_id
    post['title'] = title
    post['user_id'] = wiz.session.get('id')
    post['priority'] = priority
    post['content'] = content
    post['updated'] = datetime.datetime.now()

    boarddb.update(post, id=post_id)

    wiz.response.status(200, True)
    
def delete():
    board_id = wiz.request.query("id", True)
    boarddb.delete(id=board_id)
    wiz.response.status(200)