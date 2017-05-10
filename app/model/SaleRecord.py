from .. import db


class SaleRecord(db.Model):
    __tablename__ = "app_sale_record"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('app_product.id'))
    customer_phone = db.Column(db.String(11), nullable=False)
    customer_name = db.Column(db.String(64), nullable=False)
    valid = db.Column(db.Boolean, default=False)
    award = db.Column(db.Float)
