import scrypt
import base64
from flask import request
from jwcrypto import jwk, jwt
from globals import app, Session, key
from models import User


@app.route('/')
def hello_world():
    # import pdb; pdb.set_trace()
    for instance in User.query.all():
        return str(instance.id) + ":" + instance.username
    return "Home"


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    verify_user(request.form['jwt'],
                'abc')
    return "done"


@app.route('/update')
def update_item():
    return "update"


@app.route('/query')
def query_items():
    return "query"


@app.route('/signup', methods=['POST'])
def signup():
    given_username = request.form['username']
    given_password = base64.b64encode(scrypt.hash(base64.b64encode(request.form['password']), 'random salt'))
    ins = User(username=given_username, passhash=given_password)

    try:
        Session.add(ins)
        Session.commit()
    except Exception as ex:
        return 'Something went wrong: ' + str(ex)

    return "done"


@app.route('/login', methods=['POST'])
def login():
    # TODO: sanitize input
    given_username = request.form['username']
    given_password = base64.b64encode(scrypt.hash(base64.b64encode(request.form['password']), 'random salt'))
    res = User.query.filter_by(username=given_username).filter_by(passhash=given_password).first()

    if res:
        token = jwt.JWT(header={"alg": "HS256"},
                        claims={"info": given_username})
        token.make_signed_token(key)
        return token.serialize()

    return "None"


def verify_user(token, username):
    k = {"k": key, "kty": "oct"}
    keyx = jwk.JWK(**k)
    e = token
    ET = jwt.JWT(key=keyx, jwt=e)
    ST = jwt.JWT(key=keyx, jwt=ET.claims)
    return ST.claims


if __name__ == '__main__':
    app.run()
