from . import Base
from sqlalchemy import *

class Nastavnik(Base):
    __tablename__ = "nastavnici"
    ID_nastavnika = Column(Integer, primary_key=True)
    ime = Column(String(25))
    prezime = Column(String(25))
    email = Column(String(100))
    titula = Column(String(20))

