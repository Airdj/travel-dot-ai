import pandas as pd
import time
from api_management import get_nearby_locations


def get_as_much_data_as_possible(city_name, entity_type):
    data_response = get_nearby_locations(city_name, ent_type=entity_type)
    if data_response:
        next_page_token = data_response.get('next_page_token')
        df = pd.DataFrame(
            data_response.get('results', 'N/A'))
        while next_page_token:
            time.sleep(3)
            another_request = get_nearby_locations(
                city_name, ent_type=entity_type, next_pt=next_page_token)
            next_page_data = pd.DataFrame(another_request.get('results',
                                                              'N/A'))
            next_page_token = another_request.get('next_page_token')
            df = pd.concat([df, next_page_data])

        return df

    else:
        return 'N/A'


def data_cleaner(df):
    new_df = df.reset_index()
    new_df.rename(columns={'place_id': 'place_id_string'}, inplace=True)
    new_df['types'] = new_df['types'].astype(str)\
                                     .str.strip('[]')\
                                     .str.replace("'", "")
    new_df = new_df[['place_id_string', 'name', 'rating', 'user_ratings_total',
                    'types']]

    return new_df
