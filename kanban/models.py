from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from kanban.database import db


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    photo: Mapped[str]
    create_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now())
    update_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now())
    cards: Mapped[List['Card']] = relationship(back_populates='user')

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.id)


class Card(Base):
    __tablename__ = 'cards'
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]
    create_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now())
    update_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='cards')
    category: Mapped['CardCategory'] = relationship(back_populates='card')


class CardCategory(Base):
    __tablename__ = 'cards_categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    create_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now())
    update_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now())
    card_id: Mapped[int] = mapped_column(ForeignKey('cards.id'))
    card: Mapped['Card'] = relationship(back_populates='category')


Base.metadata.create_all(db)
