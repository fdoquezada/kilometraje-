from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    is_admin: Optional[int] = 0


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class KilometrajeBase(BaseModel):
    fecha: str
    patente: str
    km_entrada:float
    km_salida: float
    total_km:float


class Kilometraje(KilometrajeBase):
    id: int
    user_id: int
    

    class Config:
       orm_mode = True     


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None              