from . import Base
from sqlalchemy import *

class Raspored (Base):
    __tablename__ = "raspored"
    ID_raspored = Column(Integer, primary_key =True)
    dan = Column(Date)
    pocetak = Column(DateTime)
    kraj = Column(DateTime)

    nastavnik_id = Column(Integer, ForeignKey('nastavnici.ID_nastavnika'))
    predmet_id = Column(Integer, ForeignKey('predmeti.ID_predmeta'))
