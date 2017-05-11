from .. import db


class Product(db.Model):
    __tablename__ = "app_product"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    type = db.Column(db.String(64), nullable=False)
    award = db.Column(db.Float)
    update_time = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    sale_records = db.relationship('SaleRecord', backref='app_product', lazy='dynamic')
