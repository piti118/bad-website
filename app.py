from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

posts = []
app = Flask('bad-website')
app.secret_key = "super secret key"
dbfile = 'badwebsites.db'


@app.route('/', methods=["GET"])
def index():
    return redirect(url_for('login_get'))


@app.route('/login', methods=["GET"])
def login_get():
    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    # THIS IS A SUPER BAD IDEA
    # INJECT COMMAND in password " or ""="
    # OR EVEN password x"; UPDATE votes SET vote=9999 WHERE name="Pepsi";SELECT "
    query = 'SELECT * from users where username="' + username + '" AND password = "' + password + '"'
    result = execute(query)
    if len(result) > 0:  # good?? not really..
        session['username'] = username
        return redirect(url_for('vote_get'))
    else:  # bad password
        return render_template('login.html', flash="Wrong username or password!")


@app.route('/logout', methods=["get"])
def logout():
    session.clear()
    return redirect(url_for('login_get'))


########## VOTING


@app.route('/vote', methods=["GET"])
def vote_get():
    if is_logged_in():
        return render_template('vote.html', vr=vote_results())
    else:
        return redirect(url_for('login_get'))


@app.route('/vote', methods=["POST"])
def vote_post():
    if is_logged_in():
        name = request.form['name']
        query = 'UPDATE votes SET vote = vote + 1 WHERE name = "' + name + '"'
        execute(query)
        return redirect(url_for('vote_get'))
    else:
        return redirect(url_for('login_get'))


######## Wall (XSS Vulnerbilities)

@app.route('/wall', methods=["GET"])
def wall_get():
    return render_template('wall.html', msg=fetch_all_walls())


@app.route('/wall', methods=["POST"])
def wall_post():
    msg = request.form['msg']
    post_wall(msg)
    return redirect(url_for('wall_get'))


@app.route('/reset-wall', methods=["GET"])
def reset_wall():
    execute('DELETE from wall')
    return redirect(url_for('wall_get'))


### Utilities

#this is a terrible idea for excuting sql statements
def execute(query):
    rows = []
    with sqlite3.connect(dbfile) as conn:
        c = conn.cursor()
        for q in query.split(';'):
            print(q)
            c.execute(q)
            rows = c.fetchall()
        conn.commit()
        c.close()
    return rows


def is_logged_in():
    return 'username' in session


def vote_results():
    return execute('SELECT name, vote from votes')


def fetch_all_walls():
    return execute('SELECT msg from wall ORDER BY id DESC')


def post_wall(msg):
    with sqlite3.connect(dbfile) as conn:
        c = conn.cursor()
        print('hello')
        c.execute('INSERT INTO wall (msg) VALUES (?)', (msg,))
        rows = c.fetchall()
        conn.commit()
        c.close()
    return rows


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
