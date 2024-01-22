from flask import request, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from httpx import Client
from wtforms import PasswordField, SelectField, StringField
from wtforms.validators import DataRequired


class CategoryField(SelectField):
    def __init__(self, *args, **kwargs):
        with_nothing = kwargs.get('with_nothing')
        if with_nothing:
            del kwargs['with_nothing']
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
            if with_nothing:
                self.choices.insert(0, (0, 'Nenhuma'))


class CreateTaskForm(FlaskForm):
    title = StringField('Titulo', validators=[DataRequired()])
    category = CategoryField('Categoria', validators=[DataRequired()], with_nothing=True)


class CreateCategoryForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])


class DeleteCategoryForm(FlaskForm):
    category = CategoryField('Categoria', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password_confirmation = PasswordField(
        'Confirmação de Senha', validators=[DataRequired()]
    )
