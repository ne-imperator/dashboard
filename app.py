from flask import Flask, request
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
            password = row[1]
            users_dict[username] = password

    return users_dict


def show_the_login_form():
    return app.send_static_file('form.html')


def do_the_login(username, input_password):
    users_dict = load_beta_users(beta_users_filename)
    if username not in users_dict:
        return app.send_static_file('error.html')
    password = users_dict[username]
    if password != input_password:
        return app.send_static_file('error.html')

    return app.send_static_file('private.html')


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        return do_the_login(username, password)
    else:
        return show_the_login_form()


if __name__ == '__main__':
    app.run()
