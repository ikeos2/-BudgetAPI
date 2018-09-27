from jwcrypto import jwt
from models import BooksMembers
from globals import key
import string
import json


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


# extract user ID from JWT
def get_user_id(token):
    e = token
    et = jwt.JWT(key=key, jwt=e)
    st = jwt.JWT(key=key, jwt=et.claims)

    parsed_json = json.loads(st.claims)

    return parsed_json['id']
    # no_digits = string.printable[10:]
    # trans = str.maketrans(no_digits, " " * len(no_digits))  # Need to convert to am actual number
    # return token.translate(trans).split()[0]
