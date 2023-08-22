import datetime

orm = wiz.model("orm")
commentdb = orm.use("comment")
user_db = orm.use("user")
wiz.session = wiz.model("session").use()

def load():
    board_id = wiz.request.query("board_id", True)
    comment = commentdb.rows(board_id=board_id, orderby="created", order="ASC")
    
    for i in range(len(comment)):
        comment[i]['user'] = user_db.get(id=comment[i]['user_id'], fields="id,name,email")
    
    login = wiz.session.get()

    wiz.response.status(200, {
        "comment": comment,
        "login": login,
    })

def upload():
    board_id = wiz.request.query("id", True)
    text = wiz.request.query("content", True)

    if (text[-1] == '\n'):
        text = text[:-1]

    comment = dict()
    comment['board_id'] = board_id
    comment['user_id'] = wiz.session.get('id')
    comment['content'] = text
    comment['created'] = datetime.datetime.now()
    commentdb.insert(comment)

    wiz.response.status(200, True)

def update():
    comment_id = wiz.request.query("id", True)
    comment = commentdb.get(id=comment_id)

    if comment['status'] == 'show':
        data = dict()
        data['status'] = 'edit'
        commentdb.update(data, id=comment_id)
    else:
        content = wiz.request.query("text", True)
        data = dict()
        data['status'] = 'show'
        data['content'] = content
        data['updated'] = datetime.datetime.now()
        commentdb.update(data, id=comment_id)

    wiz.response.status(200, True)


def delete():
    comment_id = wiz.request.query("id", True)

    # data = dict()
    # data['status'] = 'delete'
    # commentdb.update(data, id=comment_id)

    commentdb.delete(id=comment_id)

    wiz.response.status(200, True)
