import scrypt
import base64
import json
from flask import request, abort
from jwcrypto import jwt
from globals import app, Session, key
from models import User, Transaction
from transactions import add_transaction
from utils import get_claims, verify_book_access, verify_user, get_user_id
# import pdb; pdb.set_trace()


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    valid = verify_user(request.headers['jwt'])
    if valid:
        return "done"
    abort(401)


@app.route('/transaction', methods=['POST', 'PUT', 'DELETE', 'GET'])
def transaction():
    if verify_user(request.headers['jwt']):
        if request.method == 'POST':
            return add_transaction(request, Session)
        elif request.method == 'PUT':
            return "2"
        elif request.method == 'DELETE':
            return "3"
        elif request.method == 'GET':
            book_id = request.args.get('book_id')
            user_id = get_user_id(request.headers['jwt'])

            verify_book_access(book_id, user_id)
            return json.dumps([i.serialize for i in Transaction.query.filter_by(book_id=book_id)])
        return "0"
    return '-1'


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
    # TODO: load hash from file
    given_password = base64.b64encode(scrypt.hash(base64.b64encode(request.form['password']), 'random salt'))
    res = User.query.filter_by(username=given_username).filter_by(passhash=given_password).first()

    if res:
        token = jwt.JWT(header={"alg": "HS256"},
                        claims={"username": given_username, "id": res.id})
        token.make_signed_token(key)
        encrypted_token = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512"},
                                  claims=token.serialize())
        encrypted_token.make_encrypted_token(key)
        return encrypted_token.serialize()
    return "None"


@app.route('/debug')
def debug():
    return_val = "JWT claims:\n"

    e = request.headers['jwt']
    et = jwt.JWT(key=key, jwt=e)
    st = jwt.JWT(key=key, jwt=et.claims)

    return_val += st.claims
    return return_val


if __name__ == '__main__':
    app.run()
