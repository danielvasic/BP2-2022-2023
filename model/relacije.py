from sqlalchemy.orm import relationship

from .ucenik import Ucenik
from .izostanak import Izostanak
from .razred import Razred
from .predmet import Predmet
from .nastavnik import Nastavnik
from .raspored import Raspored
from .ocjena import Ocjena

Ucenik.razred = relationship("Razred", back_populates="ucenici")
Ucenik.ocjene = relationship("Ocjena", back_populates="ucenik")
Ucenik.izostanci = relationship("Izostanak", back_populates="ucenik")
Izostanak.ucenik = relationship("Ucenik", back_populates="izostanci")
Razred.ucenici = relationship("Ucenik", back_populates="razred")
Raspored.predmet = relationship("Predmet", back_populates = "sati")
Raspored.nastavnik = relationship("Nastavnik", back_populates="sati")
Predmet.sati = relationship("Raspored", back_populates = "predmet")
Predmet.ocjene = relationship("Ocjena", back_populates="predmet")
Ocjena.ucenik = relationship("Ucenik", back_populates="ocjene")
Ocjena.predmet = relationship("Predmet", back_populates="ocjene") 
Nastavnik.sati = relationship("Raspored", back_populates = "nastavnik")