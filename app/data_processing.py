import pandas as pd
from api_management import get_nearby_locations


def get_as_much_data_as_possible():
    data_response = get_nearby_locations(radius='20000')
    if data_response:
        next_page_token = data_response.get('next_page_token')
        df = pd.DataFrame(data_response.get('results', 'Oops, could not get that :('))
        return df
    else:
        return 'Sorry :('



if __name__ == '__main__':
    print(get_as_much_data_as_possible())