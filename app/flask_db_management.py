from flask_db import City, PlaceAround, GeneratedPropositions,   \
    PropositionData
from sqlalchemy import exists
from api_management import get_city_coordinates
from data_processing import get_as_much_data_as_possible, data_cleaner
from config import types_of_ent
import pandas as pd
import hashlib
from tqdm import tqdm
from app import db


def insert_city(name, loc):
    new_city = City(city_name=name, localisation=loc)
    db.session.add(new_city)
    db.session.commit()

    return new_city


def insert_place_around(df, new_city):
    for _, row in df.iterrows():
        new_place = PlaceAround(name=row['name'],
                                place_id_string=row['place_id_string'],
                                rating=row['rating'],
                                user_ratings_total=row['user_ratings_total'],
                                types=row['types'])
        new_place.city = new_city
        db.session.add(new_place)
        db.session.commit()


def insert_generated_proposition(gen_hash, mean, median):
    new_generated_proposition = GeneratedPropositions(
        proposition_hash=gen_hash,
        rating_mean=mean,
        rating_median=median)
    db.session.add(new_generated_proposition)
    db.session.commit()

    return new_generated_proposition


def insert_proposition_data(df, generated_proposition):
    for _, row in df.iterrows():
        new_data = PropositionData(name=row['name'],
                                   place_id=row['place_id'],
                                   place_id_string=row['place_id_string'],
                                   rating=row['rating'],
                                   user_ratings_total=row[
                                       'user_ratings_total'],
                                   types=row['types'])
        new_data.hash = generated_proposition
        db.session.add(new_data)
        db.session.commit()


def get_total_data(city_to_add):
    city_loc = get_city_coordinates(city_to_add)
    reformatted_loc = str(city_loc.get('lat')) + ',' + str(city_loc.get(
        'lng'))
    data_to_concat = []
    for item in tqdm(types_of_ent):
        try:
            data_to_concat.append(data_cleaner(get_as_much_data_as_possible
                                               (city_to_add, item)))
        except Exception:
            pass
    total_data = pd.concat(data_to_concat).drop_duplicates().reset_index()
    insert_place_around(total_data, insert_city(city_to_add, reformatted_loc))
    return total_data


def final_prompter_by_loc_flask(city_prompt):
    try:
        city_loc = get_city_coordinates(city_prompt)
        reformatted_loc = str(city_loc.get('lat')) + ',' + str(city_loc.get(
            'lng'))
        ret = db.session.query(exists().where(City.localisation ==
                                              reformatted_loc)).scalar()
        if ret:
            city_selected = db.session.query(PlaceAround) \
                .join(City) \
                .filter(City.localisation == reformatted_loc)
            df = pd.read_sql_query(city_selected.statement,
                                   con=db.engine)
            return df.sample(n=10)
        else:
            print('Please wait. It might take a while...')
            get_total_data(city_prompt)
            city_selected = db.session.query(PlaceAround) \
                .join(City) \
                .filter(City.localisation == reformatted_loc)
            df = pd.read_sql_query(city_selected.statement,
                                   con=db.engine)
            return df.sample(n=10)
    except Exception:
        print('Sorry, something went wrong :(')


def data_aftermarket(df, score_point):
    algo = hashlib.sha256()
    text = ''.join(df['place_id_string'].sort_values())
    algo.update(bytes(text, encoding='utf-8'))
    algo_hash = algo.hexdigest()
    data_mean = df['rating'].mean()
    data_median = df['rating'].median()

    ret = db.session.query(exists().where(
        GeneratedPropositions.proposition_hash == algo_hash)).scalar()
    if ret:
        proposition_selected = db.session.query(
            GeneratedPropositions).filter(
            GeneratedPropositions.proposition_hash == algo_hash).first()
        proposition_selected.score += score_point
        db.session.commit()
    else:
        proposition = insert_generated_proposition(algo_hash, data_mean,
                                                   data_median)
        insert_proposition_data(df, proposition)
