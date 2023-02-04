from flask import Flask, render_template, flash, request

DEBUG = True
SECRET_KEY = 'kcneuehd739fnt56ggcxswecy2409vur'

app = Flask(__name__)
app.config.from_object(__name__)


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
    return render_template('contact.html')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title="Page not found"), 404


if __name__ == "__main__":
    app.run(debug=True)
