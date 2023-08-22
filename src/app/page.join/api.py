import datetime
import re

orm = wiz.model("orm")
userdb = orm.use("user")
verifydb = orm.use("verify")

def sendmail(user):
    title = "[KMBIG] 회원가입 이메일 인증 안내"
    message = "KMBIG 회원가입을 위한 메일 인증입니다. <br>"
    message += "서비스를 이용하시려면 아래의 인증 코드를 입력해주세요. <br><br>"
    message += f"<div style='display: flex; margin-top: 12px;'><span style='line-height: 1.4666667; color: #000000; text-align: center; border: 0px solid transparent; padding: .375rem 1rem; font-size: .875rem; border-radius: 3px; transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out; color: #000000; background-color: #EDEEF8; border-color: #D1D4DA; font-weight: 500; display: inline-block; align-items: center; justify-content: center; width: 100%;'>인증코드: {user['code']}</span></div>"

    smtp = wiz.model("portal/season/smtp").use()
    smtp.send(user['email'], template="default", title=title, message=message)
    return wiz.response.status(200, True)

def check():
    mail = wiz.request.query('mail', True)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", mail):
        return wiz.response.status(401, '잘못된 이메일 형식입니다.')

    user = userdb.get(email=mail)

    # 이미 가입되있거나 가입 진행중인 경우
    if user is not None:
        return wiz.response.status(401, '이미 가입된 이메일입니다.')

    wiz.model('orm').use('verify').update({'status': 'expired'}, email=mail)

    verify = dict()
    verify['email'] = mail
    verify['status'] = 'active'
    verify['code'] = orm.random(6, number=True)
    verify['created'] = datetime.datetime.now()
    verify['updated'] = datetime.datetime.now()
    verifydb.insert(verify)
    return sendmail(verify)

def resend():
    mail = wiz.request.query('mail', True)
    print(mail)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", mail):
        return wiz.response.status(401, '잘못된 이메일 형식입니다.')

    wiz.model('orm').use('verify').update({'status': 'expired'}, email=mail)

    user = userdb.get(email=mail)
    verify = verifydb.get(email=mail)

    # 회원 정보 확인
    if verify is None:
        return wiz.response.status(404, "가입되지 않은 회원입니다.")
    if user is not None:
        return wiz.response.status(401, '이미 가입된 이메일입니다.')
    
    # 인증 코드 생성
    verify = dict()
    verify['email'] = mail
    verify['status'] = 'active'
    verify['code'] = orm.random(6, number=True)
    verify['created'] = datetime.datetime.now()
    verify['updated'] = datetime.datetime.now()
    verifydb.insert(verify)
    return sendmail(verify)

def verify():
    mail = wiz.request.query('mail', True)
    code = wiz.request.query('code', True)

    # 이메일 형식 확인
    if not re.match(r"[^@]+@[^@]+\.[^@]+", mail):
        return wiz.response.status(401, '잘못된 이메일 형식입니다.')

    # 사용자 정보 불러오기
    user = userdb.get(email=mail)
    verify = verifydb.get(email=mail, status="active")

    # 회원 정보 확인
    if verify is None:
        return wiz.response.status(404, "가입되지 않은 회원입니다.")
    if user is not None:
        return wiz.response.status(401, '이미 가입된 이메일입니다.')

    if verify['code'] != code:
        return wiz.response.status(404, "잘못된 인증번호 입니다.")
    
    diff = (datetime.datetime.now() - verify['created']).total_seconds()
    if diff > 60 * 10:
        return wiz.response.status(401, "인증 유효 시간이 초과되었습니다. 다시 시도해주세요.")

    wiz.model('orm').use('verify').update({'status': 'verified'}, email=mail, status='active')

    wiz.session.set(verified=mail)
    return wiz.response.status(200, True)

    

def join():
    mail = wiz.request.query('mail', True)
    # verified = wiz.session.get("verified")
    # if verified != mail:
    #     return wiz.response.status(401, "잘못된 접근입니다")

    user = wiz.request.query()
    user['id'] = mail.split('@')[0]
    user['email'] = user['mail']
    user['created'] = datetime.datetime.now()
    user['updated'] = datetime.datetime.now()
    user['role'] = 'user'
    userdb.insert(user)
    wiz.session.clear()
    return wiz.response.status(200, True)