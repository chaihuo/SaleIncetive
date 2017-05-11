# -*- coding: utf-8 -*-
from .. import db
from app.model.Product import Product
from app.model.User import User


class SaleRecord(db.Model):
    __tablename__ = "app_sale_record"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('app_product.id'))
    customer_phone = db.Column(db.String(11), nullable=False)
    customer_name = db.Column(db.String(64), nullable=False)
    time = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    valid = db.Column(db.Integer, default=0)  # 0待审核， 1审核通过， -1审核不通过
    award = db.Column(db.Float)

    def get_user(self):
        user = User.query.get(self.user_id)
        return user


    def get_product(self):
        product = Product.query.get(self.product_id)
        return product
