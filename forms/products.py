from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class ProductsForm(FlaskForm):
    product = StringField('Товар', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
