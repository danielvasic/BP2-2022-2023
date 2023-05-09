from . import Base
from sqlalchemy import *

class Predmet (Base):
    __tablename__ = "predmeti"
    ID_predmeta = Column(Integer, primary_key=True)
    naziv = Column(String(75))
    opis = Column(Text)