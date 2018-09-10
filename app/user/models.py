from app import db
from flask_bcrypt import Bcrypt
from flask import  abort, current_app
from datetime import datetime, timedelta
from app.models import Base
import jwt

class User(Base):
    """ This represents the User model """

    __tablename__ = 'users'

    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    user_name = db.Column(db.String(15), unique=True) #default will be email
    textmps = db.relationship(
        'TextMP', order_by='TextMP.id', cascade="all, delete-orphan")
    imagemps = db.relationship(
        'ImageMP', order_by='ImageMP.id', cascade="all, delete-orphan")
    quip = db.Column(db.String(500), nullable=True)
    photo = db.Column(db.String(100))
    location = db.Column(db.String(25))
    deleted = db.Column(db.Boolean(), default=False)
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

    def generate_token(self, user_id):
        """ Generate the access token """

        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=10), # should be until sign out or browser is closed
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm="HS256"
            )

            return jwt_string
        
        except Exception as e:
            return str(e)

    @staticmethod
    def get(email):
        user = User.query.filter_by(email=email).first()
        if user.deleted:
            abort(404)
        return user

    def delete(self):
        user = User.query.filter_by(email=self.email).first()
        if user.deleted:
            abort(404)
        user.deleted = True
        db.session.commit()

    def __repr__(self):
        return "<User: {}>".format(self.email)

    @staticmethod
    def decode_token(token):
        """Decodes access token from Auth header"""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"
