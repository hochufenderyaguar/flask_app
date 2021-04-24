from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms import SubmitField


class ProductsAddForm(FlaskForm):
    product = StringField('Товар', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class ProductsEditForm(FlaskForm):
    price = IntegerField('Цена', validators=[DataRequired()])
    submit = SubmitField('Изменить')
