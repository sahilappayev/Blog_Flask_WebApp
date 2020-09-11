from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from passlib.hash import bcrypt
from forms import RegisterForm
from db import insert

app = Flask(__name__)

# index page
@app.route("/")
def index():
       return render_template("index.html")

# register page
@app.route("/register", methods = ["GET", "POST"])
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

        insert(name=name, surname=surname, age=age, username=username,email=email,password=password)

        return redirect(url_for("index"))
    else:
        return render_template("register.html", form = form)


# abou page
@app.route("/about")
def about():
    return render_template("about.html")

# article page
@app.route("/article/<string:id>")
def article(id):
    return 'Article id: ' + id


if(__name__ == "__main__"):
    app.run(debug=True)