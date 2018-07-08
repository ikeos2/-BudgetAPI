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
    category_id = Column(Integer)
    image = Column(LargeBinary)
    date_modified = Column(DateTime)
    book_id = Column(Integer)

    @property
    def serialize(self):
        return {
            'id':  self.id,
            'date': self.date.__str__(),
            'amount': self.amount,
            'comment': self.comment,
            'category_id': self.category_id,
            'image': self.image,
            'date_modified': self.date_modified,
            'book_id': self.book_id
        }

    def __repr__(self):
        return self.serialize()

    def __str__(self):
        return str(self.__repr__)
