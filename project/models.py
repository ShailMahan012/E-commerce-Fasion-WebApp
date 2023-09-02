from project import db
from werkzeug.security import generate_password_hash, check_password_hash


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

    def __str__(self):
        return f"{self.title}, {self.price}, {self.core_collection}"

class Images(db.Model):
    __tablename__ = 'Images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, default=None)
    title = db.Column(db.Text, nullable=False)
    filename = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=None)
    def __str__(self):
        return f"{self.id}, {self.product_id}, {self.title}, {self.order}"

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

    note = db.Column(db.Text, default=None)
    status = db.Column(db.Boolean, nullable=True, default=False)

class Cart(db.Model):
    __tablename__ = 'Cart'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Admin(db.Model):
    __tablename__ = "Admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    def set_user(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def verify(self, password):
        if check_password_hash(self.password_hash, password):
            return True
        return False

    def __str__(self):
        return f"USERNAME: {self.username} HASH: {self.password_hash}"
