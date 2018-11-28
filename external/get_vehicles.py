import requests
import json
import arrow

from collections import defaultdict
from connect_db import get_db
from constants import (
    GET_ROUTES_ENDPOINT,
    GET_VEHICLES_ENDPOINT,
)

mapping = {
    'RouteKey':'RouteKey',
    'DirectionKey':'DirectionKey'
}

vehicle_pattern_mapping = {
    'Pattern.Key': 'PatternKey',
    'Pattern.Name': 'PatternName',
    'Pattern.Direction.DirectionName': 'PDirectionName'
}

vehicle_mapping = {
    'Key': 'VehicleKey',
    'Name': 'VehicleName',
    'PercentFilled': 'PercentFilled',
    'GPS.Date': 'GpsDate',
    'GPS.Lat': 'GpsLat',
    'GPS.Long': 'GpsLong',
    'GPS.Spd': 'GpsSpd',
    'GPS.Dir': 'GpsDir',
    'Route.Key': 'RouteKey',
    'Route.Name': 'RouteName',
    'Route.ShortName': 'RouteShortName',
    'NextStop.Key': 'NextStopKey',
    'NextStop.Name': 'NextStopName',
    'NextStop.ArrivalAtStop': 'NextStopArrivalAtStop',
    'NextStop.TimeToStop': 'NextStopTimeToStop',
    'NextStop.IsTimePoint': 'NextStopIsTimePoint',
    'NextStop.StopCode': 'NextStopStopCode',
    'NextStop.EstimatedDepartTime': 'NextStopEstimatedDepartTime',
    'NextStop.ScheduledWorkDate': 'NextStopScheduledWorkDate',
    'RequestedStop': 'RequestedStop',
    'IsLastVehicle': 'IsLastVehicle',
    'PassengerCapacity': 'PassengerCapacity',
    'PassengersOnboard': 'PassengersOnboard',
    'Work': 'Work'     
}

def transform_date(str_date):
    if not str_date:
        # sometimes NextStop* returns {}
        return str_date
    return arrow.get(str_date).datetime

transform_mapping = defaultdict(lambda: lambda x: x)
transform_mapping['GpsDate'] = transform_date
transform_mapping['NextStopTimeToStop'] = transform_date
transform_mapping['NextStopEstimatedDepartTime'] = transform_date
transform_mapping['NextStopScheduledWorkDate'] = transform_date
transform_mapping['NextStopArrivalAtStop'] = transform_date

def get_veh_data(dct, layers):
    if dct is None:
        return {}
    if isinstance(layers, str):
        return dct[layers]
    if layers:
        k = layers.pop(0)
        return get_veh_data(dct[k], layers)
    return dct
        
def filter_vehicles(r):
    veh_filtered = []
    for dct_item in r:
        veh_fil = {}
        try:
            for route_key, final_key in mapping.items():
                veh_fil[final_key] = get_veh_data(
                    dct_item,
                    route_key.split('.') if '.' in route_key else route_key
                )

            for pattern_item in dct_item['VehiclesByPattern']:
                for route_key, final_pattern_key in vehicle_pattern_mapping.items():
                    veh_fil[final_pattern_key] = get_veh_data(
                        pattern_item,
                        route_key.split('.') if '.' in route_key else route_key
                    )
                for veh_item in pattern_item['Vehicles']:
                    for veh_key, final_veh_key in vehicle_mapping.items():
                        veh_fil[final_veh_key] = get_veh_data(
                            veh_item,
                            veh_key.split('.') if '.' in veh_key else veh_key
                        )
            veh_fil = {k: transform_mapping[k](v) for k, v in veh_fil.items()}
            veh_filtered.append(veh_fil)
        except Exception as e:
            # TODO: use logging
            print(
                f'Something went wrong in get_all_vehicles '
                f'but need to try other items: {e}'
            )

    return veh_filtered 

def get_all_vehicles():
    # GetRoutes
    route_r = requests.post(GET_ROUTES_ENDPOINT)
    route_data = route_r.json()

    # GetVehicles
    vehicle_array = []
    for route_item in route_data:
        try:
            direction_value = route_item['PatternList'][0]['Direction']['DirectionKey']
            route_value = route_item['Key']
            vehicle_params = (
                f'routeDirectionKeys[0][RouteKey]={route_value}&'
                f'routeDirectionKeys[0][DirectionKey]={direction_value}'
            )
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            vehicle_r = requests.post(
                GET_VEHICLES_ENDPOINT,
                data=vehicle_params,
                headers=headers,
            )
            vehicle_data = vehicle_r.json()
            vehicle_draft = json.dumps(vehicle_data)
            vehicle = json.loads(vehicle_draft)
            vehicle_array = vehicle_array + vehicle
        except Exception as e:
            # TODO: use logging
            print(
                f'Something went wrong in get_all_vehicles '
                f'but need to try other items: {e}'
            )

    return filter_vehicles(vehicle_array)


if __name__ == "__main__":
    db = get_db()
    db.vehicles.insert_many(get_all_vehicles())    
