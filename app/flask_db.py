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
    