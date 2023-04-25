from . import Base
from model.ucenik import Ucenik
from sqlalchemy import *
from sqlalchemy.orm import relationship

class Razred (Base):
    ID_razreda = Column(Integer, primary_key =True)
    godina = Column(Integer)
    odjeljenje = Column(String(5))

    ucenici = relationship("Ucenik", back_populates="razred")