from flask import Flask, render_template, flash, request, g, abort
import os
import sqlite3
from FDataBase import FDataBase

DATABASE = 'fitsite.db'
DEBUG = True
SECRET_KEY = 'kcneuehd739fnt56ggcxswecy2409vur'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fitsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


dbase = None


@app.before_request
def before_reqest():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


def del_db(id_row):
    db = sqlite3.connect("fitsite.db")
    c = db.cursor()
    c.execute(f"DELETE FROM posts WHERE id = '{id_row}'")
    db.commit()
    db.close()


@app.route("/home")
@app.route("/")
def index():

    return render_template('index.html')


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        if len(request.form['name']) >= 2 and len(str(request.form['phone'])) >= 9:
            flash('Thank you, we will contact you soon', category='success')
        else:
            flash('Send error!', category='error')
    return render_template('contact.html', title="Contact")


@app.route("/blog")
def blog():

    return render_template('blog.html', title="Blog", posts=dbase.getPostsAnonce())


@app.route("/post/<alias>")
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)
    return render_template("post.html", title=title, post=post)


@app.route("/test")
def test():
    title, post = dbase.getPost("flask")
    return render_template("post.html", title=title, post=post)


@app.route("/add_blog", methods=['POST', 'GET'])
def add_blog():
    if request.method == "POST":
        if len(request.form['name']) > 3 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Error adding article!', category='error')
            else:
                flash('Article added successfully!', category='success')
        else:
            flash('Error adding article!', category='error')
    return render_template('add_blog.html', title="Add Blog")


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="Page not found"), 404


@app.route("/working_on_it")
def working_on_it():

    return render_template('work-page.html', title="Sorry...")


if __name__ == "__main__":
    app.run(debug=True)
