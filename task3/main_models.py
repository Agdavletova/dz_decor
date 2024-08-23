import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Book, Publisher, Sale, Stock, Shop
from task2 import task2

password = "123aisly"
db_name = "test_orm"
db_user = "postgres"

DSN = f"postgresql://{db_user}:{password}@localhost:5432/{db_name}"

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()


# #
# a1 = Publisher(name="Издательство 1")
# session.add(a1)
# session.commit()
#
# b1 = Book(title="Непоседа", id_publisher=a1.id)
# b2 = Book(title="Луки", id_publisher=a1.id)
#
# session.add(b1)
# session.add(b2)
# session.commit()
#
# shop1 = Shop(name="Магазин1")
# shop2 = Shop(name="Магазин2")
# session.add_all([shop1, shop2])
# session.commit()
#

@task2.logger("models.log")
def get_shops(p):
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale,
                      ).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if p.isdigit():
        publisher = session.query(Publisher).filter(Publisher.id == int(p)).first()
    else:
        publisher = session.query(Publisher).filter(Publisher.name == p).first()

    if publisher:
        for book_title, shop_name, price, date_sale in q.filter(Publisher.id == publisher.id):
            print(f"{book_title: <40} | {shop_name: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}")
    else:
        print("Нет такого издательства")


if __name__ == '__main__':
    pub = input("Введите название или идентификатор издательства: ")
    get_shops(pub)

# session.query(Sale).delete()
# session.query(Stock).delete()
# session.query(Shop).delete()
# session.query(Book).delete()
# session.query(Publisher).delete()
# session.commit()

session.close()
