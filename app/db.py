from sqlalchemy import MetaData, Table, Column, Integer, Numeric, String, \
    ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, backref, \
    sessionmaker
from config import username, password

your_username = username
your_password = password

Base = declarative_base()
engine = create_engine(f'postgresql+psycopg2://{your_username}:{your_password}'
                       f'@/travel_dot_ai_db?host=/var/run/postgresql')
Session = sessionmaker(bind=engine)
session = Session()


class City(Base):
    __tablename__ = 'cities'

    city_id = Column(Integer(), primary_key=True)
    city_name = Column(String(100), index=True)
    localisation = Column(String(100))


class PlaceAround(Base):
    __tablename__ = 'places_around'

    place_id = Column(Integer(), primary_key=True)
    city_id = Column(Integer(), ForeignKey('cities.city_id'))
    name = Column(String(100))
    place_id_string = Column(String(500))
    rating = Column(Numeric())
    user_ratings_total = Column(Numeric())
    types = Column(String(500))

    city = relationship('City', backref=backref('places_around'))





if __name__ == '__main__':
    connection = engine.connect()
    Base.metadata.create_all(engine)