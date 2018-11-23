import requests
import json

from connect_db import get_db
from constants import GET_ROUTES_ENDPOINT

mapping = {
    'Key':'RouteKey',
    'Name':'RouteName',
    'ShortName':'RouteShortName',
    'Description':'RouteDescription', 
}

pattern_mapping = {
    'Key': 'PatternListKey',
    'Direction.DirectionKey': 'DDirectionKey',
    'Direction.DirectionName': 'DDirectionName',
}

def get_data(dct, layers):
    if isinstance(layers, str):
        return dct[layers]
    
    if layers:
        k = layers.pop(0)
        return get_data(dct[k], layers)
    return dct
        
def filter_routes(r):
    route_filtered = []
    for dct_item in r:
        route_fil = {}
        for route_key, final_key in mapping.items():
            route_fil[final_key] = get_data(
                dct_item,
                route_key.split('.') if '.' in route_key else route_key
            )
        for pattern_item in dct_item['PatternList']:
            for route_key, final_pattern_key in pattern_mapping.items():
                route_fil[final_pattern_key] = get_data(
                    pattern_item,
                    route_key.split('.') if '.' in route_key else route_key
                )
        route_filtered.append(route_fil)
    return route_filtered   

def get_all_routes():
    # GetRoutes
    route_r = requests.post(GET_ROUTES_ENDPOINT)
    route_data = route_r.json()
    return filter_routes(route_data)


if __name__ == "__main__":
    db = get_db()
    db.routes.insert_many(get_all_routes())
