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
    title = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text)
    price = db.Column(db.Integer)
    details = db.Column(db.Text, nullable=False)
    core_collection = db.Column(db.Boolean, nullable=False)

    primary = db.Column(db.Integer, nullable=False)
    secondary = db.Column(db.Integer, nullable=False)

class Images(db.Model):
    __tablename__ = 'Images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, default=None)
    title = db.Column(db.Text, nullable=False)
    filename = db.Column(db.Text, nullable=False)

class Orders(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)

    f_name = db.Column(db.Text, nullable=False)
    l_name = db.Column(db.Text, nullable=True)

    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)

class Cart(db.Model):
    __tablename__ = 'Cart'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

