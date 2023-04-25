
from . import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from model.ucenik import Ucenik
from model.predmet import Predmet

class Ocjena (Base):
    ID_ocjene = Column(Integer, primary_key = True)
    ocjena = Column(Integer)
    opis = Column(Text)
    datum = Column(DateTime)

    ucenik = relationship("Ucenik", back_populates="ocjene")
    predmet = relationship("Predmet", back_populates="ocjene") 