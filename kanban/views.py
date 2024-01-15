from datetime import datetime
from uuid import uuid4

from flask import jsonify, request
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from kanban.database import Session
from kanban.models import Card, CardCategory, User


def required_fields(*args):
    def decorator(function):
        for arg in args:
            if request.json.get(arg) is None:
                return jsonify({'error': f'required field "{arg}"'}), 400
        return function()

    return decorator


def token_required(function):
    def decorator(function):
        with Session() as session:
            if request.json.get('token') is None:
                return jsonify({'error': 'required field "token"'}), 400
            query = select(User).where(User.token == request.json['token'])
            user = session.scalars(query).first()
            if user:
                return function()
            else:
                return jsonify({'error': 'invalid token'}), 400

    return decorator


def init_app(app):
    @required_fields('name', 'email', 'password')
    @app.post('/user')
    def create_user():
        with Session() as session:
            token = uuid4()
            user = User(
                name=request.json['name'],
                email=request.json['email'],
                password=generate_password_hash(request.json['password']),
                token=token,
                photo=request.json.get('photo'),
            )
            session.add(user)
            session.commit()
            session.flush()
            return jsonify(user.to_dict())

    @required_fields('name', 'password', 'email', 'photo', 'cards_ids')
    @token_required
    @app.put('/user')
    def update_user():
        with Session() as session:
            query = select(User).where(User.token == request.json['token'])
            user = session.scalars(query).first()
            cards = [
                card
                for card in session.scalars(select(Card))
                if card.id in request.json['cards_ids']
            ]
            user.name = request.json['name']
            user.password = request.json['password']
            user.email = request.json['email']
            user.photo = request.json['photo']
            user.update_at = datetime.now()
            user.cards = cards
            return jsonify(user.to_dict())

    @token_required
    @app.get('/card')
    def get_cards():
        with Session() as session:
            cards = [
                card.to_dict() for card in session.scalars(select(Card)).all()
            ]
            return jsonify(cards)

    @token_required
    @app.get('/card/<int:card_id>')
    def get_card(card_id):
        with Session() as session:
            card = session.get(Card, card_id)
            if card:
                return jsonify(card.to_dict())
            else:
                return jsonify({'error': 'card not found'}), 404

    @required_fields('title', 'description', 'category_id')
    @token_required
    @app.post('/card')
    def create_card():
        with Session() as session:
            query = select(User).where(User.token == request.json['token'])
            user = session.scalars(query).first()
            category = session.get(CardCategory, request.json['category_id'])
            if category is None:
                return jsonify({'error': 'invalid category_id'}), 400
            card = Card(
                status='todo',
                title=request.json['title'],
                description=request.json['description'],
                category_id=category.id,
                user_id=user.id,
            )
            session.add(card)
            session.commit()
            session.flush()
            return jsonify(card.to_dict())

    @required_fields('status')
    @token_required
    @app.put('/card')
    def update_card():
        with Session() as session:
            card = session.get(Card, request.json['card_id'])
            if request.json['status'] not in ['todo', 'doing', 'done']:
                return (
                    jsonify(
                        {
                            'error': 'card status should only be todo, doing or done'
                        }
                    ),
                    400,
                )
            if card:
                card.status = request.json['status']
                card.title = request.json['title']
                card.description = request.json['description']
                card.update_at = datetime.now()
                card.category_id = request.json['category_id']
                session.commit()
                session.flush()
                return jsonify(card.to_dict())
            else:
                return jsonify({'error': 'card not found'}), 404

    @token_required
    @app.get('/card-category')
    def get_cards_categories():
        with Session() as session:
            cards_categories = [
                card_category.to_dict()
                for card_category in session.scalars(
                    select(CardCategory)
                ).all()
            ]
            return jsonify(cards_categories)

    @token_required
    @app.get('/card-category/<int:card_category_id>')
    def get_card_category(card_category_id):
        with Session() as session:
            card_category = session.get(CardCategory, card_category_id)
            if card_category:
                return jsonify(card_category.to_dict())
            else:
                return jsonify({'error': 'card category not found'}), 404

    @required_fields('name')
    @token_required
    @app.post('/card-category')
    def create_card_category():
        with Session() as session:
            card_category = CardCategory(name=request.json['name'])
            session.add(card_category)
            session.commit()
            session.flush()
            return jsonify(card_category.to_dict())

    @required_fields('card_category_id', 'name')
    @token_required
    @app.put('/card-category')
    def update_card_category():
        with Session() as session:
            card_category = session.get(
                CardCategory, request.json['card_category_id']
            )
            if card_category:
                card_category.name = request.json['name']
                card_category.update_at = datetime.now()
                session.commit()
                session.flush()
                return jsonify(card_category.to_dict())
            else:
                return jsonify({'error': 'card category not found'}), 404
