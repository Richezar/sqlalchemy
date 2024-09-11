import datetime
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=20), unique=True, nullable=False)

class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), nullable=False, unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='books')

    def __str__(self):
        return self.title

class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=20), unique=True, nullable=False)

    def __str__(self):
        return self.name


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref='books')
    shop = relationship(Shop, backref='shops')

class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.String, nullable=False)
    date_sale = sq.Column(sq.DateTime, default=datetime.datetime.now())
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref='stocks')

    def __str__(self):
        return self.price

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

