
from . import Base
from sqlalchemy import *

class Ocjena (Base):
    __tablename__ = "ocjene"
    ID_ocjene = Column(Integer, primary_key = True)
    ocjena = Column(Integer)
    opis = Column(Text)
    datum = Column(DateTime)

    ucenik_id = Column(Integer, ForeignKey('ucenici.ID_ucenika'))
    predmet_id = Column(Integer, ForeignKey('predmeti.ID_predmeta'))