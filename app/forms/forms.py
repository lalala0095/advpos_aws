from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class AccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo('password', message="Passwords must match.")
    ])
    name = StringField("Account Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    subscription = SelectField("Subscription Model", choices=[
        ("free", "Free"),
        ("basic", "Basic"),
        ("premium", "Premium")
    ])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[
            DataRequired(message="Username is required"), 
            Length(min=4, max=25)
        ]
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(message="Password is required")]
    )
    submit = SubmitField('Login')