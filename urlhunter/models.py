from datetime import datetime
from hashlib import md5
from urlhunter.extensions import db, login
from werkzeug import security
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    urls = db.relationship('Url', backref='owner')
    regexs = db.relationship('Regex', backref='author')

    def set_password(self, password):
        self.password_hash = security.generate_password_hash(password)

    def check_password(self, password):
        return security.check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Regex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    site = db.Column(db.String(120))
    body = db.Column(db.String(120))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
