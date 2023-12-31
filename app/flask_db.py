from app import db


class City(db.Model):
    __tablename__ = 'cities'

    city_id = db.Column(db.Integer(), primary_key=True)
    city_name = db.Column(db.String(200), index=True)
    localisation = db.Column(db.String(200))

    def __repr__(self):
        return f"City(city_id='{self.city_id}'," \
               f"city_name='{self.city_name}'," \
               f"localisation='{self.localisation}'"


class PlaceAround(db.Model):
    __tablename__ = 'places_around'

    place_id = db.Column(db.Integer(), primary_key=True)
    city_id = db.Column(db.Integer(), db.ForeignKey(
        'cities.city_id'))
    name = db.Column(db.String(200))
    place_id_string = db.Column(db.String(500))
    rating = db.Column(db.Numeric())
    user_ratings_total = db.Column(db.Numeric())
    types = db.Column(db.String(500))

    city = db.relationship('City')

    def __repr__(self):
        return f"PlaceAround(place_id= '{self.place_id}'," \
               f"city_id= '{self.city_id}'," \
               f"name= '{self.name}'," \
               f"place_id_string= '{self.place_id_string}'," \
               f"rating= '{self.rating}'," \
               f"user_ratings_total= '{self.user_ratings_total}'," \
               f"types= '{self.types}')"


class GeneratedPropositions(db.Model):
    __tablename__ = 'generated_propositions'

    proposition_hash = db.Column(db.String(200), primary_key=True, index=True)
    rating_mean = db.Column(db.Float())
    rating_median = db.Column(db.Float())
    score = db.Column(db.Integer(), default=0)

    def __repr__(self):
        return f"Hash(proposition_hash='{self.proposition_hash}'," \
               f"rating_mean='{self.rating_mean}'," \
               f"rating_median='{self.rating_median}'"


class PropositionData(db.Model):
    __tablename__ = 'proposition_data'

    id = db.Column(db.Integer(), primary_key=True)
    place_id = db.Column(db.Integer())
    proposition_hash = db.Column(db.Float(), db.ForeignKey(
        'generated_propositions.proposition_hash'))
    name = db.Column(db.String(200))
    place_id_string = db.Column(db.String(500))
    rating = db.Column(db.Numeric())
    user_ratings_total = db.Column(db.Numeric())
    types = db.Column(db.String(500))

    hash = db.relationship('GeneratedPropositions')

    def __repr__(self):
        return f"PropositionData(proposition_hash= " \
               f"'{self.proposition_hash}'," \
               f"name= '{self.name}'," \
               f"place_id_string= '{self.place_id_string}'," \
               f"rating= '{self.rating}'," \
               f"user_ratings_total= '{self.user_ratings_total}'," \
               f"types= '{self.types}')"
