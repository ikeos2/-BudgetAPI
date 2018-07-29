import scrypt
import base64
import json
import string
from flask import request, abort
from jwcrypto import jwt
from globals import app, Session, key
from models import User, Transaction, BooksMembers


# import pdb; pdb.set_trace()



global image_name
image_name = 0

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
            if request.form.get('amount') is None or len(request.form.get('amount')) < 1:
                return "Amount is required"
            if request.form.get('date') is None or len(request.form.get('date')) < 1:
                return "Date is required"
            if request.form.get('book_id') is None or len(request.form.get('book_id')) < 1:
                return "Book id is required"

            kws = {"amount":  float(request.form['amount']),
                   "date": request.form['date'],
                   "book_id": request.form['book_id'],
                   "comment": request.form.get('comment'),
                   "category_id": request.form.get('category_id')}

            if request.form.get('image') is not None:
                path = str(image_name) + ".gif"
                image_name += 1
                file = open(path, "w")
                img_data = base64.b64decode(request.form.get('image'))
                file.write(img_data)
                file.close()
                kws = {"image": image_name}
            try:
                # trans = Transaction(amount=float(request.form['amount']),
                #                     date=request.form['date'],
                #                     book_id=request.form['book_id'],
                #                     comment=request.form.get('comment'),
                #                     category_id=request.form.get('category_id'))
                trans = Transaction(kws)
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

            no_digits = string.printable[10:]
            trans = str.maketrans(no_digits, " "*len(no_digits))  # Need to convert to am actual number
            user_id = get_claims(request.headers['jwt']).translate(trans).split()[0]

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
    ET = jwt.JWT(key=key, jwt=e)
    ST = jwt.JWT(key=key, jwt=ET.claims)

    return_val += ST.claims
    return return_val


def get_claims(token):
    if len(token) > 0:
        try:
            e = token
            ET = jwt.JWT(key=key, jwt=e)
            ST = jwt.JWT(key=key, jwt=ET.claims)
            return ST.claims
        except Exception:
            return {}
    return {}

# If the JWT is valid, then we don't need to verify the data
def verify_user(token):
    if len(token) > 0:
        try:
            e = token
            ET = jwt.JWT(key=key, jwt=e)
            ST = jwt.JWT(key=key, jwt=ET.claims)
            return True
        except Exception:
            return False
    return False


# Check that a given user had access to a specific book
def verify_book_access(book_id, user_id):
    res = BooksMembers.query.filter_by(book_id=book_id).filter_by(user_id=user_id).first()
    if res:
        return True
    return False

if __name__ == '__main__':
    app.run()

