from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from passlib.hash import bcrypt
from forms import RegisterForm, LoginForm, ArticleForm
from db import insert_user, user_login, insert_article, select_articles, select_articles_by_outhor, select_article_by_id, delete_article_by_id
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
    articles = select_articles_by_outhor(session['user_id'])
    if articles:
        return render_template('dashboard.html', articles = articles)
    else:
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

# articles page
@app.route("/articles")
def articles():
    articles = select_articles()
    if articles:
        return render_template('articles.html', articles = articles)
    else:
        return render_template('articles.html')

# article page
@app.route("/article/<string:id>")
def article(id):
    article = select_article_by_id(id)
    if articles:
        return render_template('article.html', article = article)
    else:
        return render_template('article.html')

# delete article
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    result = delete_article_by_id(id)
    if articles:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))


if(__name__ == "__main__"):
    app.run(debug=True)
