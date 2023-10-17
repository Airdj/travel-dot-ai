from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, \
    create_engine, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
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


class GeneratedPropositions(Base):
    __tablename__ = 'generated_propositions'

    proposition_hash = Column(String(200), primary_key=True, index=True)
    rating_mean = Column(Float())
    rating_median = Column(Float())
    score = Column(Integer(), default=0)

    def __repr__(self):
        return f"Hash(proposition_hash='{self.proposition_hash}'," \
               f"rating_mean='{self.rating_mean}'," \
               f"rating_median='{self.rating_median}'"


class PropositionData(Base):
    __tablename__ = 'proposition_data'

    id = Column(Integer(), primary_key=True)
    place_id = Column(Integer())
    proposition_hash = Column(String(), ForeignKey(
        'generated_propositions.proposition_hash'))
    name = Column(String(200))
    place_id_string = Column(String(500))
    rating = Column(Numeric())
    user_ratings_total = Column(Numeric())
    types = Column(String(500))

    hash = relationship('GeneratedPropositions')

    def __repr__(self):
        return f"PropositionData(proposition_hash= " \
               f"'{self.proposition_hash}'," \
               f"name= '{self.name}'," \
               f"place_id_string= '{self.place_id_string}'," \
               f"rating= '{self.rating}'," \
               f"user_ratings_total= '{self.user_ratings_total}'," \
               f"types= '{self.types}')"


if __name__ == '__main__':
    connection = engine.connect()
    Base.metadata.create_all(engine)
