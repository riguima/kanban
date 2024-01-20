from datetime import datetime
from functools import wraps
from uuid import uuid4

from flask import Blueprint, jsonify, request
from sqlalchemy import select

from kanban.database import Session
from kanban.models import Category, Task, User

bp = Blueprint('api', __name__, url_prefix='/api')


def required_fields(*fields):
    def decorator(function, *args, **kwargs):
        @wraps(function)
        def inner():
            for field in fields:
                if request.json.get(field) is None:
                    return jsonify({'error': f'required field "{field}"'}), 400
            return function(*args, **kwargs)

        return inner

    return decorator


def token_required(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        with Session() as session:
            if request.method != 'GET':
                if request.json.get('token') is None:
                    return jsonify({'error': 'required field "token"'}), 400
                query = select(User).where(User.token == request.json['token'])
            else:
                if request.args.get('token') is None:
                    return jsonify({'error': 'required field "token"'}), 400
                query = select(User).where(User.token == request.args['token'])
            user = session.scalars(query).first()
            if user is None:
                return jsonify({'error': 'invalid token'}), 400
            return function(*args, **kwargs)

    return decorator


@bp.get('/user')
@token_required
def get_user():
    with Session() as session:
        query = select(User).where(User.token == request.args['token'])
        user = session.scalars(query).first()
        return jsonify(user.to_dict())


@bp.post('/user')
@required_fields('name', 'email', 'password')
def create_user():
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


@bp.put('/user')
@token_required
@required_fields('name', 'password', 'email', 'tasks_ids')
def update_user():
    with Session() as session:
        query = select(User).where(User.token == request.json['token'])
        user = session.scalars(query).first()
        tasks = [
            task
            for task in session.scalars(select(Task)).all()
            if task.id in request.json['tasks_ids']
        ]
        user.name = request.json['name']
        user.password = request.json['password']
        user.email = request.json['email']
        user.photo = request.json.get('photo')
        user.update_at = datetime.now()
        user.tasks = tasks
        session.commit()
        session.flush()
        return jsonify(user.to_dict())


@bp.delete('/user')
@token_required
def delete_user():
    with Session() as session:
        query = select(User).where(User.token == request.json['token'])
        user = session.scalars(query).first()
        session.delete(user)
        session.commit()
        session.flush()
        return jsonify(user.to_dict())


@bp.get('/task')
@token_required
def get_tasks():
    with Session() as session:
        query = select(User).where(User.token == request.args['token'])
        user = session.scalars(query).first()
        query = select(Task).where(Task.user_id == user.id)
        tasks = [task.to_dict() for task in session.scalars(query).all()]
        return jsonify(tasks)


@bp.get('/task/<int:task_id>')
@token_required
def get_task(task_id):
    with Session() as session:
        query = select(User).where(User.token == request.args['token'])
        user = session.scalars(query).first()
        task = session.get(Task, task_id)
        if task and task.user_id == user.id:
            return jsonify(task.to_dict())
        else:
            return jsonify({'error': 'task not found'}), 404


@bp.post('/task')
@token_required
@required_fields('title', 'category_id')
def create_task():
    with Session() as session:
        query = select(User).where(User.token == request.json['token'])
        user = session.scalars(query).first()
        category = session.get(Category, request.json['category_id'])
        if category is None:
            return jsonify({'error': 'invalid category_id'}), 400
        task = Task(
            status='todo',
            title=request.json['title'],
            description=request.json.get('description'),
            category_id=category.id,
            user_id=user.id,
        )
        session.add(task)
        session.commit()
        session.flush()
        return jsonify(task.to_dict())


@bp.put('/task')
@token_required
@required_fields('id', 'status', 'title', 'category_id')
def update_task():
    with Session() as session:
        task = session.get(Task, request.json['id'])
        if request.json['status'] not in ['todo', 'doing', 'done']:
            return (
                jsonify(
                    {'error': 'task status should only be todo, doing or done'}
                ),
                400,
            )
        if task:
            task.status = request.json['status']
            task.title = request.json['title']
            task.description = request.json.get('description')
            task.update_at = datetime.now()
            task.category_id = request.json['category_id']
            session.commit()
            session.flush()
            return jsonify(task.to_dict())
        else:
            return jsonify({'error': 'task not found'}), 404


@bp.delete('/task')
@token_required
@required_fields('id')
def delete_task():
    with Session() as session:
        task = session.get(Task, request.json['id'])
        if task is None:
            return jsonify({'error': 'task not found'}), 404
        session.delete(task)
        session.commit()
        session.flush()
        return jsonify(task.to_dict())


@bp.get('/category')
@token_required
def get_categories():
    with Session() as session:
        query = select(User).where(User.token == request.args['token'])
        user = session.scalars(query).first()
        query = select(Category).where(Category.user_id == user.id)
        categories = [
            category.to_dict() for category in session.scalars(query).all()
        ]
        return jsonify(categories)


@bp.get('/category/<int:category_id>')
@token_required
def get_category(category_id):
    with Session() as session:
        query = select(User).where(User.token == request.args['token'])
        user = session.scalars(query).first()
        category = session.get(Category, category_id)
        if category and category.user_id == user.id:
            return jsonify(category.to_dict())
        else:
            return jsonify({'error': 'task category not found'}), 404


@bp.post('/category')
@token_required
@required_fields('name')
def create_category():
    with Session() as session:
        query = select(User).where(User.token == request.json['token'])
        user = session.scalars(query).first()
        category = Category(name=request.json['name'], user_id=user.id)
        session.add(category)
        session.commit()
        session.flush()
        return jsonify(category.to_dict())


@bp.put('/category')
@token_required
@required_fields('id', 'name')
def update_category():
    with Session() as session:
        category = session.get(Category, request.json['id'])
        if category:
            category.name = request.json['name']
            category.update_at = datetime.now()
            session.commit()
            session.flush()
            return jsonify(category.to_dict())
        else:
            return jsonify({'error': 'category not found'}), 404


@bp.delete('/category')
@token_required
@required_fields('id')
def delete_category():
    with Session() as session:
        category = session.get(Category, request.json['id'])
        if category is None:
            return jsonify({'error': 'category not found'}), 404
        session.delete(category)
        session.commit()
        session.flush()
        return jsonify(category.to_dict())
