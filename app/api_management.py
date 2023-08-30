import requests
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
        print(err, 'Oops, connection went wrong :(')


def get_city_coordinates(city_name):
    response = requests.get(f'https://maps.googleapis.com/maps/api/place'
                            f'/findplacefromtext'
                            f'/json?input={city_name}&'
                            f'inputtype=textquery&fields=formatted_address%2C'
                            f'name%2Crating'
                            f'%2Copening_hours%2Cgeometry&key={YOUR_API_KEY}')

    if response.json().get('status') == 'OK':
        location = response.json()['candidates'][0]['geometry']['location']
        return location


def get_nearby_locations(city_name,
                         next_pt=None,
                         ent_type='',
                         radius='10000'):
    cords = get_city_coordinates(city_name)
    if cords:
        location = 'location=' + str(cords.get('lat')) + ',' + str(
            cords.get('lng'))

        params = {'type': ent_type,
                  'radius': radius,
                  'key': YOUR_API_KEY,
                  'pagetoken': next_pt
                  }

        response = requests.get(f'https://maps.googleapis.com/maps/api/place'
                                f'/nearbysearch/json?{location}',
                                params=params)

        return response.json()


def get_place_info(place_id):
    params = {'place_id': place_id,
              'language': 'en',
              'reviews_no_translations': False,
              'key': YOUR_API_KEY}

    response = requests.get('https://maps.googleapis.com/maps/api/place/'
                            'details/json?', params=params)

    return response.json().get('result', 'N/A')
