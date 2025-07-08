from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Integer, default=0)  # 0 = usuario normal, 1 = admin
    
    # Fechas con timezone-aware
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

class Kilometraje(Base):
    __tablename__ = "kilometraje"
    
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    patente = Column(String, nullable=False)
    km_entrada = Column(Integer, nullable=False)
    km_salida = Column(Integer, nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    def __repr__(self):
        return f"Kilometraje(id={self.id}, fecha={self.fecha}, patente={self.patente}, km_entrada={self.km_entrada}, km_salida={self.km_salida}, usuario_id={self.usuario_id})"