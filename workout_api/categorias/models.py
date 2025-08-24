from sqlalchemy import Integer, String, DateTime
from workout_api.contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
#from workout_api.atleta.models import AtletaModel

class CategoriaModel(BaseModel):
    
    __tablename__ = 'categorias'
    
    pk_id:  Mapped[int]   = mapped_column(Integer,    primary_key=True)
    nome:   Mapped[str]   = mapped_column(String(50), unique=True, nullable=False)    
    atleta: Mapped['AtletaModel'] = relationship(back_populates='categoria')    
    
#    created_at:Mapped[datetime] = mapped_column(DateTime, nullable=False)
