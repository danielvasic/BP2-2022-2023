from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("mysql://root:csdigital@localhost:3306/bp2", echo=True)
Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()

class User (Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    lastname = Column(String(50))

    addresses = relationship("Address", back_populates="user")

    def __str__(self):
        return self.name + " " + self.lastname

class Address(Base):
    __tablename__="addresses"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="addresses")

Base.metadata.create_all(engine)
