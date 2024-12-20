from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField, DateField, FloatField
from wtforms.validators import DataRequired, Optional

class COGsForm(FlaskForm):
    date_of_transaction = DateField("Date of Transaction", validators=[DataRequired()])
    description = StringField("Items or Description", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    type_of_goods = SelectField("Type of Goods", choices=[
        ('', 'Select an option'),
        ("Raw Materials", "Raw Materials"),
        ("Packaging", "Packaging"),
        ("Transportation Expense", "Transportation Expense"),
        ("Courier Service", "Courier Service"),
        ("Others", "Others")
    ])
    platform = SelectField("Platform", choices=[
        ('', 'Select an option'),
        ("Shopee", "Shopee"),
        ("Tiktok", "Tiktok"),
        ("Lazada", "Lazada"),
        ("Physical Store", "Physical Store"),
        ("Others", "Others")
    ], validators=[Optional()])
    store = StringField("Store")
    payment_method = StringField("Payment Method")
    remarks = StringField("Remarks")
    submit = SubmitField("Submit")

class COGsUpdateForm(FlaskForm):
    date_of_transaction = DateField("Date of Transaction")
    description = StringField("Items or Description")
    price = FloatField("Price")
    type_of_goods = SelectField("Type of Goods", choices=[
        ('', 'Select an option'),
        ("Raw Materials", "Raw Materials"),
        ("Packaging", "Packaging"),
        ("Transportation Expense", "Transportation Expense"),
        ("Courier Service", "Courier Service"),
        ("Others", "Others")
    ])
    platform = SelectField("Platform", choices=[
        ('', 'Select an option'),
        ("Shopee", "Shopee"),
        ("Tiktok", "Tiktok"),
        ("Lazada", "Lazada"),
        ("Physical Store", "Physical Store"),
        ("Others", "Others")
    ], validators=[Optional()])
    store = StringField("Store")
    payment_method = StringField("Payment Method")
    remarks = StringField("Remarks")
    submit = SubmitField("Submit")
