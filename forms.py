from wtforms import Form, StringField, TextAreaField, PasswordField, DateField, validators
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


class LoginForm(Form):
    username = StringField('Enter username')
    password = PasswordField('Enter password')