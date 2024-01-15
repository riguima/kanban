from datetime import datetime
from uuid import uuid4

from flask import jsonify, request
from sqlalchemy import select

from kanban.database import Session
from kanban.models import Card, CardCategory, User


def validate_fields(*fields):
    for field in fields:
        if request.json.get(field) is None:
            return jsonify({'error': f'required field "{field}"'}), 400


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
    @token_required
    @app.get('/user')
    def get_user():
        with Session() as session:
            query = select(User).where(User.token == request.json['token'])
            user = session.scalars(query).first()
            return jsonify(user.to_dict())

    @app.post('/user')
    def create_user():
        validation_response = validate_fields('name', 'email', 'password')
        if validation_response is not None:
            return validation_response
        with Session() as session:
            token = str(uuid4())
            user = User(
                name=request.json['name'],
                email=request.json['email'],
                password=request.json['password'],
                token=token,
                photo=request.json.get('photo'),
            )
            session.add(user)
            session.commit()
            session.flush()
            return jsonify(user.to_dict())

    @token_required
    @app.put('/user')
    def update_user():
        validation_response = validate_fields(
            'name', 'password', 'email', 'photo', 'cards_ids'
        )
        if validation_response is not None:
            return validation_response
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
    @app.delete('/user')
    def delete_user():
        with Session() as session:
            query = select(User).where(User.token == request.json['token'])
            user = session.scalars(query).first()
            session.delete(user)
            session.commit()
            session.flush()
            return jsonify(user.to_dict())

    @token_required
    @app.get('/card')
    def get_cards():
        with Session() as session:
            query = select(User).where(User.token == request.json['token'])
            user = session.scalars(query).first()
            query = select(Card).where(Card.user_id == user.id)
            cards = [card.to_dict() for card in session.scalars(query).all()]
            return jsonify(cards)

    @token_required
    @app.get('/card/<int:card_id>')
    def get_card(card_id):
        with Session() as session:
            query = select(User).where(User.token == request.json['token'])
            user = session.scalars(query).first()
            card = session.get(Card, card_id)
            if card and card.user_id == user.id:
                return jsonify(card.to_dict())
            else:
                return jsonify({'error': 'card not found'}), 404

    @token_required
    @app.post('/card')
    def create_card():
        validation_response = validate_fields(
            'title', 'description', 'category_id'
        )
        if validation_response is not None:
            return validation_response
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

    @token_required
    @app.put('/card')
    def update_card():
        validation_response = validate_fields(
            'id', 'status', 'title', 'description', 'category_id'
        )
        if validation_response is not None:
            return validation_response
        with Session() as session:
            card = session.get(Card, request.json['id'])
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
    @app.delete('/card')
    def delete_card():
        with Session() as session:
            validation_response = validate_fields('id')
            if validation_response is not None:
                return validation_response
            card = session.get(Card, request.json['id'])
            if card is None:
                return jsonify({'error': 'card not found'}), 404
            session.delete(card)
            session.commit()
            session.flush()
            return jsonify(card.to_dict())

    @token_required
    @app.get('/card-category')
    def get_cards_categories():
        with Session() as session:
            query = select(User).where(User.token == request.json['token'])
            user = session.scalars(query).first()
            query = select(CardCategory).where(CardCategory.user_id == user.id)
            cards_categories = [
                card_category.to_dict()
                for card_category in session.scalars(query).all()
            ]
            return jsonify(cards_categories)

    @token_required
    @app.get('/card-category/<int:card_category_id>')
    def get_card_category(card_category_id):
        with Session() as session:
            query = select(User).where(User.token == request.json['token'])
            user = session.scalars(query).first()
            card_category = session.get(CardCategory, card_category_id)
            if card_category and card_category.user_id == user.id:
                return jsonify(card_category.to_dict())
            else:
                return jsonify({'error': 'card category not found'}), 404

    @token_required
    @app.post('/card-category')
    def create_card_category():
        validation_response = validate_fields('name')
        if validation_response is not None:
            return validation_response
        with Session() as session:
            query = select(User).where(User.token == request.json['token'])
            user = session.scalars(query).first()
            card_category = CardCategory(
                name=request.json['name'], user_id=user.id
            )
            session.add(card_category)
            session.commit()
            session.flush()
            return jsonify(card_category.to_dict())

    @token_required
    @app.put('/card-category')
    def update_card_category():
        validation_response = validate_fields('id', 'name')
        if validation_response is not None:
            return validation_response
        with Session() as session:
            card_category = session.get(CardCategory, request.json['id'])
            if card_category:
                card_category.name = request.json['name']
                card_category.update_at = datetime.now()
                session.commit()
                session.flush()
                return jsonify(card_category.to_dict())
            else:
                return jsonify({'error': 'card category not found'}), 404

    @token_required
    @app.delete('/card-category')
    def delete_card_category():
        with Session() as session:
            validation_response = validate_fields('id')
            if validation_response is not None:
                return validation_response
            card_category = session.get(CardCategory, request.json['id'])
            if card_category is None:
                return jsonify({'error': 'card category not found'}), 404
            session.delete(card_category)
            session.commit()
            session.flush()
            return jsonify(card_category.to_dict())
