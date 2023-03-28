from orm import session, User


# Dodati 5 novih korisnika

#ivo = User(id=3, name="Ivo", lastname="Ivic")
#session.add(ivo)
#session.commit()

for user in session.query(User, User.id, User.name, User.lastname).filter(User.name=="Ivo").all():
    print(user.User)