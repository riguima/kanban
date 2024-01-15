from uuid import uuid4

from flask import jsonify, request
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from kanban.database import Session
from kanban.models import Card, CardCategory, User


def required_fields(*args):
    def decorator(function):
        for arg in args:
            if request.form.get(arg) is None:
                return jsonify({'error': f'required field "{arg}"'})
        return function()

    return decorator


def init_app(app):
    @required_fields('name', 'email', 'password')
    @app.post('/register')
    def register():
        with Session() as session:
            token = uuid4()
            user = User(
                name=request.form['name'],
                email=request.form['email'],
                password=generate_password_hash(request.form['password']),
                token=token,
            )
            session.add(user)
            session.commit()
            return jsonify({'token': token})

    @required_fields('token', 'title', 'description', 'category_id')
    @app.post('/add-card')
    def add_card():
        with Session() as session:
            query = select(User).where(User.token == request.form['token'])
            user = session.scalars(query).first()
            if user is None:
                return jsonify({'error': 'invalid token'})
            category = session.get(
                CardCategory, int(request.form['category_id'])
            )
            if category is None:
                return jsonify({'error': 'invalid category_id'})
            card = Card(
                status='todo',
                title=request.form['title'],
                description=request.form['description'],
                category_id=category.id,
                user_id=user.id,
            )
            session.add(card)
            session.commit()
            return jsonify({
                'id': card.id,
                'status': card.status,
                'title': card.title,
                'description': card.description,
                'create_at': card.create_at,
                'update_at': card.update_at,
                'user_id': card.user_id,
                'category_id': card.category_id,
            })
