from flask import request, url_for
from flask_wtf import FlaskForm
from flask_login import current_user
from httpx import Client
from wtforms import SelectField, StringField, PasswordField
from wtforms.validators import DataRequired


class CategoryField(SelectField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with Client() as client:
            response = client.get(
                request.url_root + url_for('api.get_categories'),
                params={'token': current_user.token},
            )
            self.choices = [
                (category['id'], category['name'])
                for category in response.json()
            ]


class CreateTaskForm(FlaskForm):
    title = StringField('Titulo', validators=[DataRequired()])
    category = CategoryField('Categoria', validators=[DataRequired()])


class CreateCategoryForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirmação de Senha', validators=[DataRequired()])
