from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Test(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __repr__(self):
        return f"""<Test (id="{self.id}", name={self.name}>"""


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(225))
    user_password = Column(String(225))
    user_salt = Column(String(225))

    def __repr__(self):
        return f"""<User (id="{self.id}", name={self.name}, user_password={self.user_password}>"""


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(225))

    def __repr__(self):
        return f"""<Room (id="{self.id}", room_name={self.room_name}>"""
