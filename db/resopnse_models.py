from pydantic import BaseModel, Required, Field


class UserResponse(BaseModel):
    id: int
    user_name: str

    class Config:
        orm_mode = True


class ChatResponse(BaseModel):
    id: int
    user_name: str

    class Config:
        orm_mode = True


class MessagesResponse(BaseModel):
    id: int
    chat_id: int
    sender: str
    receiver: str
    message: str
    message_time: int

    class Config:
        orm_mode = True
