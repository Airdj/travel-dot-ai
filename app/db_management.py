from db import session, City, PlaceAround
from api_management import get_city_coordinates
from data_processing import get_as_much_data_as_possible, data_cleaner


def insert_city(name, loc):
    new_city = City(city_name=name, localisation=loc)
    session.add(new_city)
    session.commit()

    return new_city


def insert_place_around(df, new_city):
    list_of_places = []
    for _, row in df.iterrows():
        new_place = PlaceAround(name=row['name'],
                                place_id_string=row['place_id_string'],
                                rating=row['rating'],
                                user_ratings_total=row['user_ratings_total'],
                                types=row['types'])
        new_place.city = new_city
        session.add(new_place)
        session.commit()



