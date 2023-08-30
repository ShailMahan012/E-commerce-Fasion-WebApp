from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__)
admin = Blueprint("admin", __name__, template_folder="templates")


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.app_context().push()


app.config['paypal'] = {
    "BASE_URL": "https://api-m.sandbox.paypal.com",
    "CLIENT_ID": "AaYITUxB_0he79pMHBsHSgs2c6IGRjkbbRJJ5H47mh4GcYbkeiJ60uzXRtgt4-YmmLmiC33yhJ4rrXQm",
    "APP_SECRET": "EAe0WivXOobHvPhrsVS9ObDaEaaR9pWgPXnRg5UO57m3caAqNWZd_kQf1QvgSDefqW7zurVWYtYZ8Dc-",
    "CURRENCY": "USD"
}
app.config['IMAGE_DIR'] =  'project/static/product_images'
app.config['TITLE'] = "Fashion"
app.config['PER_PAGE'] = 15

from project import routes, admin_routes
app.register_blueprint(admin)

