from db import session, City, PlaceAround


def insert_city(name, loc):
    new_city = City(city_name=name, localisation=loc)


def insert_place_around():
    pass
