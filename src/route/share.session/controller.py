wiz.session = wiz.model("session").use()
if not wiz.session.has("id"):
    wiz.response.redirect("/")