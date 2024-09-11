import json
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = 'postgresql://postgres:postgres@localhost:5432/test'
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

publisher_name = input()

result = session.query(Book, Shop, Sale, Sale.date_sale).filter(Publisher.name == publisher_name).filter(Publisher.id == Book.id_publisher).filter(Book.id == Stock.id_book).filter(Stock.id_shop == Shop.id).filter(Stock.id == Sale.id_stock).all()
for r in result:
    print(f'{r[0]} | {r[1]} | {r[2]} | {r[3]}')


session.close()