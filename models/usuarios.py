from sqlalchemy import Integer, String, DateTime, Column
from flask_login import UserMixin
from datetime import datetime
from database import db

class User(db.Model, UserMixin):
    
    __tablename__ = 'Usuario'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    email = Column(String(100), unique=True)
    senha = Column(String(255), nullable=False)
    criando_em = Column(DateTime, default=datetime.now)