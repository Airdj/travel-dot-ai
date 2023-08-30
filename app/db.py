from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, \
    create_engine
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
    city_name = Column(String(200), index=True)
    localisation = Column(String(200))

    def __repr__(self):
        return f"City(city_id='{self.city_id}'," \
               f"city_name='{self.city_name}'," \
               f"localisation='{self.localisation}'"


class PlaceAround(Base):
    __tablename__ = 'places_around'

    place_id = Column(Integer(), primary_key=True)
    city_id = Column(Integer(), ForeignKey('cities.city_id'))
    name = Column(String(200))
    place_id_string = Column(String(500))
    rating = Column(Numeric())
    user_ratings_total = Column(Numeric())
    types = Column(String(500))

    city = relationship('City')

    def __repr__(self):
        return f"PlaceAround(place_id= '{self.place_id}'," \
               f"city_id= '{self.city_id}'," \
               f"name= '{self.name}'," \
               f"place_id_string= '{self.place_id_string}'," \
               f"rating= '{self.rating}'," \
               f"user_ratings_total= '{self.user_ratings_total}'," \
               f"types= '{self.types}')"


if __name__ == '__main__':
    connection = engine.connect()
    Base.metadata.create_all(engine)
