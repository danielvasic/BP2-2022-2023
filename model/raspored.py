from . import Base
from model.predmet import Predmet
from model.nastavnik import Nastavnik
from sqlalchemy.orm import relationship
from sqlalchemy import *

class Raspored (Base):
    ID_raspored = Column(Integer, primary_key =True)
    dan = Column(Date)
    pocetak = Column(DateTime)
    kraj = Column(DateTime)

    predmet = relationship("Predmet", back_populates = "sati")
    nastavnik = relationship("Nastavnik", back_populates="sati")
