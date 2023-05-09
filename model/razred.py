from . import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

class Razred (Base):
    __tablename__ = "razredi"
    ID_razreda = Column(Integer, primary_key =True)
    godina = Column(Integer)
    odjeljenje = Column(String(5))