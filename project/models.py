from project import db


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    f_name = db.Column(db.Text, nullable=False)
    l_name = db.Column(db.Text, nullable=True)

class Products(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True, nullable=False)
    details = db.Column(db.Text, nullable=False)
    core_collection = db.Column(db.Boolean, nullable=False)

    primary = db.Column(db.Integer, nullable=False)
    secondary = db.Column(db.Integer, nullable=True)

class Images(db.Model):
    __tablename__ = 'Images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    path = db.Column(db.Text)
