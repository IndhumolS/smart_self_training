# models/user.py

from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool = False
