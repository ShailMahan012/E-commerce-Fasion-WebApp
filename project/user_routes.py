# Routes for user
from project import app, user, db
# from project.models import Products, Images, Orders, Cart, Admin
# from project.get_dict import *
from flask import render_template, request, session, redirect, json, flash
# from werkzeug.utils import secure_filename
from functools import wraps
# from base64 import b64encode, b64decode
# import os
# from time import time

@user.route("/user")
def user_page():
    return redirect("/user/login")


@user.route("/user/login")
def login():
    return render_template("login_user.html")
