from . import Base

from sqlalchemy import *
from sqlalchemy.orm import relationship

class Ucenik (Base):
    __tablename__ = "ucenici"
    ID_ucenika = Column(Integer, primary_key = True)
    ime = Column(String(50))
    prezime =Column(String(50))
    razred_id = Column(Integer, ForeignKey('razredi.ID_razreda'))



    