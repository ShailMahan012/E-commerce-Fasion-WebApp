from project import db


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    f_name = db.Column(db.Text, nullable=False)
    l_name = db.Column(db.Text, nullable=True)
