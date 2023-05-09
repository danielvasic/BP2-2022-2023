from . import Base
from sqlalchemy import *

class Izostanak (Base):
    __tablename__ = "izostanci"
    ID_izostanka = Column(Integer, primary_key=True)
    datum = Column(Date)
    opis = Column(Text)
    opavdano = Column(Boolean)

    ucenik_id = Column(Integer, ForeignKey('ucenici.ID_ucenika'))