import requests
import json
import pandas as pd
from config import API_KEY
YOUR_API_KEY = API_KEY


def api_connection_check():
    try:
        response = requests.get(f'https://maps.googleapis.com/maps/api/place'
                                f'/nearbysearch/json?location=-33.8670522,151'
                                f'.1957362&radius=500&types=restaurant&name=ha'
                                f'rbour&key={YOUR_API_KEY}')
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as err:
        print('Oops, connection went wrong :(')


def get_city_coordinates():
    city = input('Podaj nazwe miasta:')

    response = requests.get(f'https://maps.googleapis.com/maps/api/place'
                f'/findplacefromtext'
                f'/json?input={city}&'
                f'inputtype=textquery&fields=formatted_address%2Cname%2Crating'
                f'%2Copening_hours%2Cgeometry&key={YOUR_API_KEY}')

    if response.json()['status'] == 'OK':
        location = response.json()['candidates'][0]['geometry']['location']
        return location
    else:
        return 'Ooops, we could not find this city :('


def get_nearby_locations():
    cords = get_city_coordinates()
    location = 'location='+ str(cords.get('lat')) + ',' + str(cords.get('lng'))

    params = {#'types': 'restaurant',
              'radius': '5000',
              'key': YOUR_API_KEY
              }

    response = requests.get(f'https://maps.googleapis.com/maps/api/place'
                            f'/nearbysearch/json?{location}', params=params)

    df = pd.DataFrame(response.json()['results'])

    return df


def get_place_info():
    params = {#'place_id': place_id,
              'language': 'en',
              'reviews_no_translations': False,
              'key': YOUR_API_KEY}

    response = requests.get('https://maps.googleapis.com/maps/api/place/'
                            'details/json?place_id=ChIJU3DpyxBbFkcRZJt4gU0Poqo'
                            , params=params)

    return response.json()


if __name__ == '__main__':
    test2 = get_place_info()['result']
    print(test2['reviews'])

