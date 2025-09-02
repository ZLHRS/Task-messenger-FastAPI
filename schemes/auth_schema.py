from pydantic import BaseModel


class LoginBase(BaseModel):
    username: str
    password: str

class CurrentUser(BaseModel):
    user_id: int
    username: str
