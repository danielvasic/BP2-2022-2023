from model import *
from model.relacije import *

ucenik = Ucenik(ime="Pero", prezime="Perić")
session.add(ucenik)
session.commit()