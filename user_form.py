from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, Optional, URL


# validators
required = InputRequired()
email_validator = Email(message='Please provide a valid email address')
url_validator = URL(message='Please provide valid URL')
optional = Optional(strip_whitespace=True)
min_4 = Length(min=4)
max_50 = Length(max=50)
max_80 = Length(max=80)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        required, min_4, max_50
        ])

    password = PasswordField("Password", validators=[
        required, min_4, max_80
        ])


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
        required, min_4, max_50
        ])
    
    email = StringField("Email", validators=[
        required, 
        email_validator
        ])

    password = PasswordField("Password", validators=[
        required, min_4, max_80
        ])
