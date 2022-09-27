from pydantic import BaseModel, Required, Field


class UserModel(BaseModel):
    user_name: str = Field(Required, alias="userName")
    user_password: str = Field(Required)


class UserPasswordCredentials(BaseModel):
    user_name: str = Field(Required, alias="userName")
    password: str = Field(Required)
