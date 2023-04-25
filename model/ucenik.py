from . import Base
from model.razred import Razred
from model.ocjena import Ocjena
from model.izostanak import Izostanak

from sqlalchemy import *
from sqlalchemy.orm import relationship

class Ucenik (Base):
    ID_ucenika = Column(Integer, primary_key = True)
    ime = Column(String(50))
    prezime =Column(String(50))

    razred = relationship("Razred", back_populates="ucenici")
    ocjene = relationship("Ocjena", back_populates="ucenik")
    izostanci = relationship("Izostanak", back_populates="ucenik")
    