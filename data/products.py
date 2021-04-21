import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    product = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
