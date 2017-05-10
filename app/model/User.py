# -*- coding: utf-8 -*-
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from passlib.apps import custom_app_context as pwd_context
from flask_login import UserMixin
from .. import login_manager, db


class User(UserMixin, db.Model):
    __tablename__ = 'app_user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    sale_records = db.relationship('SaleRecord', backref='app_user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = pwd_context.encrypt(password)



    """密码生成和验证"""
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
