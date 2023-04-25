from . import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from model.raspored import Raspored
from model.ocjena import Ocjena

class Predmet (Base):
    ID_predmeta = Column(Integer, primary_key=True)
    naziv = Column(String(75))
    opis = Column(Text)

    sati = relationship("Raspored", back_populates = "predmet")
    ocjene = relationship("Ocjena", back_populates="predmet")