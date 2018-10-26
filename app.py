from flask import Flask, request
from hashlib import md5
import csv

app = Flask(__name__, static_folder='/data/static')
beta_users_filename = 'users.csv'


# TODO: use postgresql instead csv
def load_beta_users(filename):
    users_dict = dict()
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            username = row[0]
            pwd_hash = row[1]
            users_dict[username] = pwd_hash

    return users_dict


def show_the_login_form():
    return app.send_static_file('form.html')


def do_the_login(username, password):
    users_dict = load_beta_users(beta_users_filename)
    if username not in users_dict:
        return app.send_static_file('error.html')
    pwd_hash = users_dict[username]
    input_pwd_hash = md5(password.encode('utf-8')).hexdigest()
    if pwd_hash != input_pwd_hash:
        return app.send_static_file('error.html')

    return app.send_static_file('private.html')


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        return do_the_login(username, password)
    else:
        return show_the_login_form()


if __name__ == '__main__':
    app.run()

