import requests
import json
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
    lat = cords.get('lat')
    lan = cords.get('lan')
    radius_in_meters = '2000'
    types = 'restaurant'
    response = requests.get(f'https://maps.googleapis.com/maps/api/place'
                            f'/nearbysearch/json?'
                            f'location={str(lat)},{str(lan)}'
                            f'&radius={radius_in_meters}'
                            f'&types={types}'
                            f'&name=harbour'
                            f'&key={YOUR_API_KEY}')
    return response.json()
if __name__ == '__main__':
    print(get_nearby_locations())