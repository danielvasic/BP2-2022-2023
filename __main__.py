from model import *
from model.relacije import *
from model.cache import region, api

#prvi_b = Razred(godina=1, odjeljenje="b")
#session.add(prvi_b)
#session.commit()

#marko = Ucenik(ime="Marko", prezime="Markić", razred_id=1)
#session.add(marko)
#session.commit()

# ucenici = session.query(Ucenik).all()

#for ucenik in ucenici: 
#    print(ucenik.ID_ucenika, ucenik.ime + " " + ucenik.prezime)
#    if(ucenik.razred):
#        print("-",str(ucenik.razred.godina) + " " + ucenik.razred.odjeljenje)

ID = 2
KEY = f'ucenik_{ID}'
pero = region.get(KEY)
print(pero)
if pero is api.NO_VALUE:
    pero = session.query(Ucenik).filter(Ucenik.ID_ucenika==ID).one()
    region.set(KEY, pero)
print(pero.ime + " " + pero.prezime)