from app import db
from flask_bcrypt import Bcrypt

class User(db.Model):
    """ This represents the User model """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    display_name = db.Column(db.String(15), unique=True) #default will be email
    textmps = db.relationship(
        'TextMP', order_by='TextMP.id', cascade="all, delete-orphan")
    imagemps = db.relationship(
        'ImageMP', order_by='ImageMP.id', cascade="all, delete-orphan")
    # followers 
    # following

    def __init__(self, email, password):
        """ Init user model with email and password """
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """ Checks the password against its hash """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """ Saves user to db, when creating or editing model """
        db.session.add(self)
        db.session.commit()

class TextMP(db.Model):
    """This class represents the TextMP table."""

    __tablename__ = 'TextMP'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(55))
    author = db.Column(db.Integer, db.ForeignKey(User.id))
    post = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    # tags - many to many
    # likes - one to many, count of user ids

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        return TextMP.query.all(author=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<TextMP: {}>".format(self.title)


class ImageMP(db.Model):
    """This class represents the ImageMP table."""

    __tablename__ = 'ImageMP'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(55))
    author = db.Column(db.Integer, db.ForeignKey(User.id))
    post = db.Column(db.String(1000)) # url to the photo
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    # tags - many to many
    # likes - one to many, count of user ids

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        return ImageMP.query.all(author=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<ImageMP: {}>".format(self.title)
    