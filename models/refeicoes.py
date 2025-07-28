from sqlalchemy import Integer, String, Boolean, DateTime, Column, ForeignKey
from datetime import datetime
from database import db

class Refeicao(db.Model):
    
    __tablename__ = 'Refeicoes'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(
        Integer,
        ForeignKey('Usuario.id', onupdate='CASCADE'),
        nullable=False
    )
    nome = Column(String(100), nullable=False)
    data_hora = Column(DateTime)
    dentro_dieta = Column(Boolean, nullable=False)
    criado_em = Column(DateTime, default=datetime.now)