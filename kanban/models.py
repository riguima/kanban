from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from kanban.database import db


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    token: Mapped[str]
    photo: Mapped[Optional[str]]
    authenticated: Mapped[Optional[bool]] = mapped_column(default=False)
    create_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )
    update_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )
    tasks: Mapped[List['Task']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    categories: Mapped[List['Category']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'email': self.email,
            'token': self.token,
            'photo': self.photo,
            'create_at': self.create_at.strftime('%d/%m/%Y %H:%M'),
            'update_at': self.update_at.strftime('%d/%m/%Y %H:%M'),
            'tasks': [task.to_dict() for task in self.tasks],
        }


class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Optional[str]] = mapped_column(default='todo')
    title: Mapped[str]
    description: Mapped[Optional[str]]
    create_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )
    update_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='tasks')
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('categories.id')
    )
    category: Mapped[Optional['Category']] = relationship(
        back_populates='tasks'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'title': self.title,
            'description': self.description,
            'create_at': self.create_at.strftime('%d/%m/%Y %H:%M'),
            'update_at': self.update_at.strftime('%d/%m/%Y %H:%M'),
            'user_id': self.user.id,
            'category_id': None if self.category is None else self.category.id,
            'category_name': ''
            if self.category is None
            else self.category.name,
        }


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    create_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )
    update_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )
    tasks: Mapped[List['Task']] = relationship(
        back_populates='category', cascade='all, delete-orphan'
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='categories')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_at': self.create_at.strftime('%d/%m/%Y %H:%M'),
            'update_at': self.update_at.strftime('%d/%m/%Y %H:%M'),
            'user_id': self.user_id,
            'tasks': [task.to_dict() for task in self.tasks],
        }


Base.metadata.create_all(db)
