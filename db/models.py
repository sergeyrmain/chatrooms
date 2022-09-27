from sqlalchemy import Column, Integer, String, BigInteger
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


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_one = Column(Integer)
    user_two = Column(Integer)

    def __repr__(self):
        return f"""<Chat (id="{self.id}", user_one={self.user_one}, user_two={self.user_two}>"""


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer)
    sender = Column(Integer)
    receiver = Column(Integer)
    message = Column(String(225))
    message_time = Column(BigInteger)


# creating tables:

'CREATE TABLE chat.users(id INT AUTO_INCREMENT PRIMARY KEY, user_name VARCHAR(255) NOT NULL UNIQUE, user_password VARCHAR(255) NOT NULL, user_salt VARCHAR(255) NOT NULL);'

'CREATE TABLE chat.chat(id INT AUTO_INCREMENT PRIMARY KEY, user_one INT NOT NULL REFERENCES users(id), user_two INT NOT NULL REFERENCES users(id));'

'CREATE TABLE chat.messages(id INT AUTO_INCREMENT PRIMARY KEY, chat_id INT NOT NULL REFERENCES chat(id), sender INT NOT NULL REFERENCES users(id), receiver INT NOT NULL REFERENCES users(id), message VARCHAR(255) NOT NULL, message_time BIGINT NOT NULL);'
