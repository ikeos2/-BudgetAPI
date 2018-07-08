import scrypt
import base64
import json
from flask import request, abort, jsonify
from jwcrypto import jwt
from globals import app, Session, key
from models import User, Transaction


# import pdb; pdb.set_trace()


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    valid = verify_user(request.form['jwt'])
    if valid:
        return "done"
    abort(401)


@app.route('/transaction', methods=['POST', 'PUT', 'DELETE', 'GET'])
def transaction():
    if verify_user(request.headers['jwt']):
        if request.method == 'POST':
            if request.form.get('amount') is None or len(request.form.get('amount')) < 1:
                return "Amount is required"
            if request.form.get('date') is None or len(request.form.get('date')) < 1:
                return "Date is required"
            if request.form.get('book_id') is None or len(request.form.get('book_id')) < 1:
                return "Book id is required"
            if request.form.get('image') is not None:
                file = open("example.gif", "w")
                img_data = base64.b64decode(request.form.get('image'))
                file.write(img_data)
                file.close()
            try:
                trans = Transaction(amount=float(request.form['amount']),
                                    date=request.form['date'],
                                    book_id=request.form['book_id'],
                                    comment=request.form.get('comment'),
                                    category_id=request.form.get('category_id'))
                Session.add(trans)
                Session.commit()
            except Exception as ex:
                return "Error adding transaction: " + str(ex)
            return "1"
        elif request.method == 'PUT':
            return "2"
        elif request.method == 'DELETE':
            return "3"
        elif request.method == 'GET':
            book_id = request.args.get('book_id')
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
    given_password = base64.b64encode(scrypt.hash(base64.b64encode(request.form['password']), 'random salt'))
    res = User.query.filter_by(username=given_username).filter_by(passhash=given_password).first()

    if res:
        token = jwt.JWT(header={"alg": "HS256"},
                        claims={"username": given_username})
        token.make_signed_token(key)
        encrypted_token = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512"},
                                  claims=token.serialize())
        encrypted_token.make_encrypted_token(key)
        return encrypted_token.serialize()
    return "None"


# If the JWT is valid, then we don't need to verify the data
def verify_user(token):
    if len(request.headers['jwt']) > 0:
        try:
            e = token
            ET = jwt.JWT(key=key, jwt=e)
            ST = jwt.JWT(key=key, jwt=ET.claims)
            return True
        except Exception:
            return False
    return False


if __name__ == '__main__':
    app.run()
