from app import db
from flask import abort, current_app
from datetime import datetime, timedelta
from app.models import Base

class ImageMP(Base):
    """This class represents the ImageMP table."""

    __tablename__ = 'ImageMP'

    title = db.Column(db.String(55))
    author = db.Column(db.Integer, db.ForeignKey(User.id))
    post = db.Column(db.String(1000)) # url to the photo
    # tags - many to many
    # likes - one to many, count of user ids

    def __init__(self, title):
        self.title = title

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        return ImageMP.query.filter_by(author=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<ImageMP: {}>".format(self.title)
    