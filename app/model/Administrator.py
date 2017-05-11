from .. import login_manager, db


class Administrator(db.Model):
    __tablename__ = "app_administrator"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def verify_password(self, password):
        return password == self.password


