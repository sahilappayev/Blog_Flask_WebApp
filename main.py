from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from passlib.hash import bcrypt
from forms import RegisterForm, LoginForm, ArticleForm
from db import insert_user, user_login, insert_article
from functools import wraps

app = Flask(__name__)
app.secret_key = 'myblogsite'

# user login check
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You have to login to access for this page!", 'danger')
            return redirect(url_for('login'))
    return decorated_function


# index page
@app.route("/")
def index():
    return render_template("index.html")

# register page
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        surname = form.surname.data
        age = form.age.data
        username = form.username.data
        email = form.email.data
        password = bcrypt.hash(form.password.data)
        print("birthday :  ", age)

        insert_user(name=name, surname=surname, age=age,
                    username=username, email=email, password=password)

        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)

# login page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        result = user_login(username, password)
        if result:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)


# logout page
@app.route('/logout', methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('index'))

# dashboard page
@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# add article
@app.route('/addarticle', methods=["GET", "POST"])
@login_required
def add_article():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data
        author = session['user_id']
        insert_article(title, content, author)
        return redirect(url_for('index'))
    else:
        return render_template('addarticle.html', form=form)


# abou page
@app.route("/about")
def about():
    return render_template("about.html")

# article page
@app.route("/articles/<string:id>")
def article(id):
    return 'Article id: ' + id


if(__name__ == "__main__"):
    app.run(debug=True)
