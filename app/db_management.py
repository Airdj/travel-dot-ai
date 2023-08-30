from db import session, City, PlaceAround
from sqlalchemy import exists
from api_management import get_city_coordinates
from data_processing import get_as_much_data_as_possible, data_cleaner
from config import types
import pandas as pd


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


def get_total_data(city_to_add):
    city_loc = get_city_coordinates(city_to_add)
    reformatted_loc = str(city_loc.get('lat')) + ',' + str(city_loc.get(
        'lng'))
    data_to_concat = []
    for i in types:
        try:
            data_to_concat.append(data_cleaner(get_as_much_data_as_possible
                                               (city_to_add, i)))
            print(f'done with {i}')
        except Exception:
            pass
    total_data = pd.concat(data_to_concat)
    total_data = total_data.reset_index()
    insert_place_around(total_data, insert_city(city_to_add, reformatted_loc))
    print('done')
    return total_data


if __name__ == '__main__':
    city_prompt = input('what city to check?').lower().strip()
    ret = session.query(exists().where(City.city_name == city_prompt)).scalar()
    if ret:
        city_selected = session.query(PlaceAround)\
                               .join(City)\
                               .filter(City.city_name == city_prompt)
        for i in city_selected:
            print(i)
    else:
        print('Please wait. It might take a while...')
        get_total_data(city_prompt)
        city_selected = session.query(PlaceAround)\
                               .join(City)\
                               .filter(City.city_name == city_prompt)
        for i in city_selected:
            print(i)
