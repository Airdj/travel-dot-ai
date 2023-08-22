import pandas as pd
import time
from api_management import get_nearby_locations


def get_as_much_data_as_possible(cityname):
    data_response = get_nearby_locations(cityname)
    if data_response:
        next_page_token = data_response.get('next_page_token')
        df = pd.DataFrame(
            data_response.get('results', 'Oops, could not get that :('))
        print(next_page_token)
        while next_page_token:
            time.sleep(3)
            print('Start')
            another_request = get_nearby_locations(
                cityname, next_pt=next_page_token)
            print(another_request)
            next_page_data = pd.DataFrame(another_request.get('results', 'Oops, could not get that :('))
            next_page_token = another_request.get('next_page_token')
            print(next_page_token)
            df = pd.concat([df, next_page_data])
            print('end')

        return df

    else:
        return 'Sorry :('


if __name__ == '__main__':

    print(get_as_much_data_as_possible('rzeszow'))