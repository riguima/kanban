import json

from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from httpx import Client
from sqlalchemy import select

from kanban.database import Session
from kanban.forms import (CreateCategoryForm, CreateTaskForm, LoginForm,
                          RegisterForm)
from kanban.models import User


def init_app(app):
    @app.get('/')
    @login_required
    def index():
        create_task_form = CreateTaskForm()
        create_category_form = CreateCategoryForm()
        with Client() as client:
            response = client.get(
                request.url_root + url_for('api.get_tasks')[1:],
                params={
                    'token': current_user.token,
                },
            )
            return render_template(
                'index.html',
                create_task_form=create_task_form,
                create_category_form=create_category_form,
                tasks=response.json(),
                tasks_json=json.dumps(response.json()),
                token=current_user.token,
                update_task_url=request.url_root
                + url_for('api.update_task')[1:],
            )

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            with Session() as session:
                query = select(User).where(User.email == request.form['email'])
                user = session.scalars(query).first()
                if user and user.password == request.form['password']:
                    user.authenticated = True
                    session.commit()
                    session.flush()
                    login_user(user, remember=True)
                    return redirect(url_for('index'))
                else:
                    return render_template(
                        'login.html', form=form, error_message='Login Inválido'
                    )
        return render_template('login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            if (
                request.form['password']
                != request.form['password_confirmation']
            ):
                return render_template(
                    'register.html',
                    form=form,
                    error_message='As senhas são diferentes',
                )
            with Client() as client:
                response = client.post(
                    request.url_root + url_for('api.create_user'),
                    json={
                        'name': request.form['name'],
                        'email': request.form['email'],
                        'password': request.form['password'],
                    },
                )
                if response.status_code == 200:
                    return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.get('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.post('/add-task')
    @login_required
    def create_task():
        form = CreateTaskForm()
        if form.validate_on_submit():
            with Client() as client:
                body = {
                    'title': request.form['title'],
                    'token': current_user.token,
                }
                if int(request.form['category']):
                    body['category_id'] = request.form['category']
                client.post(
                    request.url_root + url_for('api.create_task')[1:],
                    json=body,
                )
        return redirect(url_for('index'))

    @app.post('/add-category')
    @login_required
    def create_category():
        form = CreateCategoryForm()
        if form.validate_on_submit():
            with Client() as client:
                client.post(
                    request.url_root + url_for('api.create_category')[1:],
                    json={
                        'name': request.form['name'],
                        'token': current_user.token,
                    },
                )
        return redirect(url_for('index'))
