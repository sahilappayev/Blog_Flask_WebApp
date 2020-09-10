from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, DateField, validators
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
import datetime


class RegisterForm(Form):
    name = StringField("Enrer name", validators=[validators.DataRequired(message="Name must be insert!")])
    surname = StringField("Enrer surname", validators=[validators.DataRequired(message="Surname must be insert!")])
    age = DateField("Enter birthdate", format='%m/%d/%Y', validators=[validators.Optional()])
    username = StringField("Enter username", validators=[validators.DataRequired(message="username must be insert!"), validators.Length(min=5)])
    email = StringField("Enter email", validators=[validators.DataRequired(), validators.Email(message="Please, enter a valid email adress.")])
    password = PasswordField("Enter password", validators=[validators.DataRequired(message="Please, set a password.")])
    confirm = PasswordField("Confirm password", validators=[validators.EqualTo(fieldname='password', message='Password not confirmed!')])



class NullableDateField(DateField):
    """Native WTForms DateField throws error for empty dates.
    Let's fix this so that we could have DateField nullable."""
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist).strip()
            if date_str == '':
                self.data = None
                return
            try:
                self.data = datetime.datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid date value'))



app = Flask(__name__)

# Db configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'myblog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


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
        password = sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()

        query = "INSERT INTO user (name, surname, age, username, email, password) VALUES (%s, %s, %s, %s,%s, %s)"

        cursor.excute(query, (name, surname, age, username, email, password))
        cursor.commit()
        mysql.connection.close()

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