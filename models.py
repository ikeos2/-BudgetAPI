from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, Float
from globals import db


class User(db.Model):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    passhash = Column(LargeBinary)

    def __repr__(self):
        return "name='%s', password='%s'" % (self.username, self.passhash)


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    amount = Column(Float)
    comment = Column(String)
    category = Column(Integer)
    image_id = Column(Integer)

    def __repr__(self):
        return "Id=%s, date=%s, amount=%d"
