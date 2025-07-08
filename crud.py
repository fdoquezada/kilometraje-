from sqlalchemy.orm import Session
from models import User, Kilometraje
from schemas import UserCreate, KilometrajeBase
from auth import get_password_hash

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_all_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_kilometraje(db: Session, km: KilometrajeBase, user_id: int):
    db_km = Kilometraje(**km.dict(), user_id=user_id)
    db.add(db_km)
    db.commit()
    db.refresh(db_km)
    return db_km

def get_kilometraje_by_user(db: Session, user_id: int):
    return db.query(Kilometraje).filter(Kilometraje.user_id == user_id).all()