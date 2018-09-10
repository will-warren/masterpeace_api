from app import db
from flask import current_app
from app.models import Base
from app.user.models import User

class TextMP(Base):
    """This class represents the TextMP table."""

    __tablename__ = 'TextMP'

    title = db.Column(db.String(55))
    author = db.Column(db.Integer, db.ForeignKey(User.id))
    post = db.Column(db.String(1000))
    # tags - many to many
    # likes - one to many, count of user ids

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<TextMP: {}>".format(self.title)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        return TextMP.query.filter_by(author=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()