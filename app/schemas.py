from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title : str
    content: str
    published: bool= True

class CreatePost(PostBase):
    pass

class Post(BaseModel):
    id: int
    title:str
    content:str
    published:bool
    created_at:datetime
    class config:
        orm_mode=True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email:EmailStr
    
    
    class config:
        orm_mode=True


class UserLogin(BaseModel):
    email: EmailStr
    password:str
    
    class config:
        orm_mode=True


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None
    

