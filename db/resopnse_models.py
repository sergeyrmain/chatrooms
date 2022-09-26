from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    user_name: str

    class Config:
        orm_mode = True


class RoomsResponse(BaseModel):
    id: int
    room_name: str

    class Config:
        orm_mode = True
