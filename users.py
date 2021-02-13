import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
#создаю таблицы декларативно
Base = declarative_base()

#создаю таблицу для регистрации новых пользователей
class Users(Base):
    __tablename__='user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)


def connect_db():
    #подключаюсь к базе
    engine = sa.create_engine(DB_PATH)
    #Создаю таблицу
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():
    first_name = input("Введите имя :")
    last_name = input("Введите фамилию :")
    gender = input("Укажите ваш пол в формате Male если ты мужчина  и Female если ты женщина: ")
    email = input("Укажите электронную почту :")
    birthdate = input("Укажите дату рождения в формате ГГГГ-ММ-ДД :")
    height = input("Укажите ваш рос в метрах. Используем точку как разделитель :")

    #Создаем объект User
    user = Users(
        first_name = first_name,
        last_name = last_name,
        gender = gender,
        email= email,
        birthdate = birthdate,
        height = height
    )
    return user

def main():
    #создаю сессию
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("Данные успешно сохранены")

if __name__ == "__main__":
    main()



