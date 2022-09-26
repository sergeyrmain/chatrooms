from typing import Optional

from pydantic import BaseModel, Required, Field


class UserModel(BaseModel):
    user_name: str = Field(Required, alias="userName")
    user_password: str = Field(Required)


class RoomChat(BaseModel):
    room_name: str = Field(Required, alias="roomName")
    user_name: str = Field(Required, alias="userName")


# creating tables:
' CREATE TABLE chat.rooms (id INT AUTO_INCREMENT PRIMARY KEY, room_name VARCHAR(255) NOT NULL, user_id INT NOT NULL REFERENCES chat.users(id) ); '

'CREATE TABLE chat.users(id INT AUTO_INCREMENT PRIMARY KEY, user_name VARCHAR(255) NOT NULL UNIQUE, user_password VARCHAR(255) NOT NULL, user_salt VARCHAR(255) NOT NULL);'

'CREATE TABLE chat.messages(id INT AUTO_INCREMENT PRIMARY KEY, room_id INT NOT NULL REFERENCES chat.rooms(id), user_id INT NOT NULL REFERENCES chat.users(id), message VARCHAR(255) NOT NULL, time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);'
