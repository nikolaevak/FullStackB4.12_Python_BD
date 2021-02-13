import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
#создаю таблицы декларативно
Base = declarative_base()

#описываю таблицу с атлетами по которой будет проводиться поиск

class Athelete(Base):
    __tablename__= 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


class Users(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

    # def __repr__(self):
    #     return "<{}:{}>".format(self.id, self.first_name)


def connect_db():
    #Создаю сессию
    engine = create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():
    #Запрашиваю данные для поиска Атлета
    user_id = input("Введите идентификатор пользователя :")
    return int(user_id)


def max_datetime(user, session):
    #Поиск ближайшего атлета по дате рождения (ГГГГ-ММ-ДД)
    #Дата рождения пользователя
    ub = user.birthdate
    min_bd = None
    athelete_id = None
    athelete_birthdate = None

    ub = ub.split('-')
    ub_birthdate_str = datetime.date(int(ub[0]), int(ub[1]), int(ub[2]))

    # Дата рождения атлета
    ab_dict = {}

    for id, birthdate in session.query(Athelete.id, Athelete.birthdate):
        birthdate = birthdate.split('-')
        ab_birthdate_str = datetime.date(int(birthdate[0]), int(birthdate[1]), int(birthdate[2]))
        ab_dict[id] = ab_birthdate_str
        min_bd_result = abs(ub_birthdate_str - ab_birthdate_str)
        if not min_bd or min_bd_result < min_bd:
            min_bd = min_bd_result
            athelete_id = id
            athelete_birthdate = birthdate

    # print (str(ub_birthdate_str))
    # print(min_bd_result)
    return (athelete_id, athelete_birthdate)

def max_height(user, session):
    #Поиск ближайшего по росту Атлета
    query_athelete = session.query(Athelete).filter(Athelete.height!= None).all()
    # print(query_athelete)
    athelete_height_dict = {athelete.id: athelete.height for athelete in query_athelete}

    user_height = user.height
    min_height = None
    athelete_id = None
    athelete_height = None
    # athlete_name = None

    for id, height in athelete_height_dict.items():
        if height is None:
            continue
        height_result = abs(user_height - height)
        if not min_height or height_result < min_height:
            min_height = height_result
            athelete_id = id
            athelete_height = height
    return athelete_id, athelete_height


def main():
    session = connect_db()
    user_id = request_data()
    user = session.query(Users).filter(user_id == Users.id).first()


    if not user:
        print("По вашему запросу не нашлось пользователя")
    else:
        athelete_id, athelete_height = max_height(user, session)
        print("Ближайший по росту найденный атлет: {}, его рост {}".format(athelete_id, athelete_height))
        athelete_id, athelete_birthdate = max_datetime(user, session)
        print("Ближайший атлет по дате рождения: {}, его дата рождения {}". format(athelete_id, '-'.join(athelete_birthdate)))

if __name__ == "__main__":
    main()






