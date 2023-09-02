from project.models import Admin
from project import db

def get_user():
    username = input("USERNAME: ")
    return Admin.query.filter_by(username=username).first(), username

def new_user():
    user, username = get_user()
    if not user:
        password = input("PASSWORD: ")
        user = Admin()
        user.set_user(username, password)
        db.session.add(user)
        db.session.commit()
        print("Done Inserting New User...")
    else:
        print("User already exist!")

def update_user():
    user, username = get_user()
    if user:
        password = input("PASSWORD: ")
        user.set_user(username, password)
        db.session.commit()
        print("Done Updating User ...")
    else:
        print("User doesn't exist!")


def del_user():
    user = get_user()[0]
    if user:
        db.session.delete(user)
        db.session.commit()
        print("Done Deleting User ...")
    else:
        print("User doesn't exist!")


funcs = [new_user, update_user, del_user]

print("""1. New User
2. Update User
3. Delete User""")
i = int(input("ENTER: ")) - 1
funcs[i]()
