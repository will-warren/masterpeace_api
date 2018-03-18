from app import db

class TextMP(db.Model):
    """This class represents the TextMP table."""

    __tablename__ = 'TextMP'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(55))
    author = db.Column(db.String(25))
    post = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    # tags - many to many
    # likes - one to many, count of user ids

    def __init__(self, title):
        """initialize with title."""
        self.title = title

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return TextMP.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<TextMP: {}>".format(self.title)