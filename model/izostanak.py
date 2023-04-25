from . import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

class Izostanak (Base):
    ID_izostanka = Column(Integer, primary_key=True)
    datum = Column(Date)
    opis = Column(Text)
    opavdano = Column(Boolean)

    ucenik = relationship("Ucenik", back_populates="izostanci")