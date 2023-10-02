from project import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from sqlalchemy.ext import hybrid


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

class Variant(db.Model):
    __tablename__ = 'Variant'
    id = db.Column(db.Integer, primary_key=True)
    prd_1 = db.Column(db.Integer)
    prd_2 = db.Column(db.Integer)

class Main_Collection_Home(db.Model):
    __tablename__ = "Main_Collection_Home"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)

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
    user_id = db.Column(db.Integer, nullable=False)

    f_name = db.Column(db.Text, nullable=False)
    l_name = db.Column(db.Text, nullable=True)

    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)

    note = db.Column(db.Text, default=None)
    status = db.Column(db.Boolean, nullable=True, default=False)
    date = db.Column(db.Date, nullable=False, default=date.today())

    discount = db.Column(db.Integer, default=None)
    approved = db.Column(db.Boolean, nullable=False, default=False)

    @hybrid.hybrid_property
    def full_name(self):
        return (self.f_name + " " + self.l_name)

class Cart(db.Model):
    __tablename__ = 'Cart'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, default=None)
    size = db.Column(db.Text)

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

class Sub_Emails(db.Model):
    __tablename__ = "Sub_Emails"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)

    f_name = db.Column(db.Text, nullable=False)
    l_name = db.Column(db.Text, nullable=True)

    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify(self, password):
        if check_password_hash(self.password_hash, password):
            return True
        return False

    def __str__(self):
        return f"EMAIL: {self.email} HASH: {self.password_hash}"

class Coupons(db.Model):
    __tablename__ = "Coupons"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False) # On which thing? PurchaseAmount or FirstOrder
    type = db.Column(db.Text, default=None) # % or cash
    amount = db.Column(db.Integer, nullable=False) # % or cash
    usage_limit = db.Column(db.Integer, default=None) # Limit per user
    min_amount = db.Column(db.Integer, default=None) # Minnimum amount to use this Coupon
    max_amount = db.Column(db.Integer, default=None) # Maximum amount to use this Coupon
    status = db.Column(db.Boolean, default=True)
