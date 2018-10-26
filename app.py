from flask import Flask, request

app = Flask(__name__, static_folder='/data/static')


def show_the_login_form():
    return app.send_static_file('form.html')


def do_the_login(username, password):
    return username + ' ' + password


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

