from datetime import datetime
from website import db
from website import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_file = db.Column(db.Text, unique=True, nullable= False)
    name = db.Column(db.Text, nullable= False)
    price = db.Column(db.Float, nullable= False)
    brand = db.Column(db.Text, nullable=False)
    descr=db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Items('{self.img}','{self.name}','{self.price}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable= False)
    firstname = db.Column(db.String(30), nullable= False)
    lastname = db.Column(db.String(30), nullable= False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash=db.Column(db.String(128))
    password=db.Column(db.String(60),nullable=False)
    
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'
        self.firstname = 'Guest'

    def is_authenticated(self):
        return False

    def is_active(self):
        return False

    def is_anonymous(self):
        return True

    def get_id(self):
        return None
