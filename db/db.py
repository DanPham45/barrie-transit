"""
Here we keep any web-DB related code
"""
import json
from collections import defaultdict

from datetime import datetime
from pymongo import MongoClient


class DB:

    def __init__(self, url):
        self.url = url
        self.client = MongoClient(url)
        self.db = self.client.barrieTransit

    def close(self):
        self.client.close()

    def add_user(self, user, password):
        # TODO: maybe only one-time by script, so not explicit registration
        pass

    def has_access(self, email, raw_password):
        # TODO:
        return True

    def insert_route(self, route):
        ref = None
        if ref:
            self.db.update({'ref': ref}, {'$push': {'routes': route}})
        else:
            self.db.insert_one({'routes': [route]})

    def insert_location(self, location):
        ref = None
        if ref:
            self.db.update({'ref': ref}, {'$push': {'locations': location}})
        else:
            self.db.insert_one({'locations': [location]})

    def get_locations(self, location=None, route=None, time=None):
        return self.db.find({k: v for k, v in [
            ('location', location),
            ('route', route),
            ('time', time)
        ]})

    def get_all_routes_name(self):
        return self.db.routes.find().distinct('RouteShortName')

    def get_location_by_name(self):
        locations = self.db.vehicles.find(
            {'PatternName':{'$exists':True}},
            {'PatternName':1,'GpsDate':1,'GpsLong':1, 'GpsLat':1, '_id':0}
        )
        return [loc for loc in locations]

    def get_number_of_routes(self):
        number = self.db.routes.aggregate([
            {'$group': {'_id': {'Key':"$RouteShortName"}}},
            {'$count': "NumOfRoute"}
        ])
        return number.next()

    def get_number_of_buses(self):
        number = self.db.vehicles.aggregate([
            {'$group': {'_id': {'Key':"$VehicleKey"}}},
            {'$count': "NumOfVehicle"}
        ])
        return number.next()

    def get_days_of_tracking(self):
        dates = self.db.vehicles.aggregate([
        {
            '$group':
                {
                '_id': 'null',
                'maxDate': { '$max': "$GpsDate" },
                'minDate': { '$min': "$GpsDate" }
                }
        }])
        date_range = dates.next()
        return (date_range['maxDate'] - date_range['minDate']).days

    def get_avg_per_route(self):
        results = self.db.vehicles.aggregate([
            {'$match': {'RouteShortName': {'$exists': True, '$ne': 'null'}}},
            {'$group': {'_id': "$RouteShortName", 'avgPassengers': {'$avg': '$PassengersOnboard'}}}
        ])
        return [
            [item['_id'], item['avgPassengers']]
            for item in results
        ]

    def get_avg_route_stop(self):
        result = self.db.vehicles.aggregate([{
            '$match': {
                'GpsDir':{
                    '$exists': True, '$ne': None
                }
            }
        },
            {
                '$group': {
                    '_id': {
                        'Route': "$PatternName",
                        'Stop':"$NextStopName",
                        'Long':"$GpsLong",
                        'Lat': "$GpsLat",
                        'DateTime': "$GpsDate"
                    },
                    'AvgPassengersOnBoard': {'$avg':"$PassengersOnboard"}
                }
            }
        ])
        number_map = {}
        for item in result:
            to_unpack = item['_id']
            to_unpack.update({'avgPass': item['AvgPassengersOnBoard']})
            
            route_name = to_unpack['Route']
            number_map[route_name] = number_map.get(route_name, len(number_map) + 1)
            yield [route_name, number_map[route_name], float(to_unpack['avgPass']), to_unpack['Stop']]

    def compare_routes(self):
        result = self.db.vehicles.aggregate([
            {
                '$match': {
                    'GpsDir': { '$exists': True, '$ne': None}
                }
            },
            {
                '$group': {
                    '_id': {'Route': "$PatternName", 'Veh':"$VehicleKey", 'DateTime': "$GpsDate"},
                    'AvgPassengersOnBoard': {'$avg':"$PassengersOnboard"},
                    'AvgSpeed': {'$avg': "$GpsSpd"}
            }
            }
        ])
        for item in result:
            r = item['_id']
            r.update({'avgPass': item['AvgPassengersOnBoard']})
            r.update({'avgSpeed': item['AvgSpeed']})
            yield [r['Route'], r['avgPass'], r['avgSpeed']]

    def delay_stat_week(self):
        result = self.db.delaystatweekly.aggregate([
            {
                '$group': {
                    '_id': {'Week': "$Week"},
                    'AvgDelay': {'$avg': "$Avg Delay"},
                    'MaxDelay': {'$max': "$Avg Delay"},
                    'MinDelay': {'$min': "$Avg Delay"},
                    'AvgStop': {'$avg':"$Stopping Time"},
                    'MaxStop': {'$max': "$Stopping Time"},
                    'MinStop': {'$min': "$Stopping Time"},
                }
            }
        ])
        return result.next()

    def delay_stat_day(self):
        result = self.db.delaystatdaily.aggregate([
            {
                '$group': {
                    '_id': {'Day': "$Day"},
                    'AvgDelay': {'$avg': "$Avg Delay"},
                    'MaxDelay': {'$max': "$Avg Delay"},
                    'MinDelay': {'$min': "$Avg Delay"},
                    'AvgStop': {'$avg':"$Stopping Time"},
                    'MaxStop': {'$max': "$Stopping Time"},
                    'MinStop': {'$min': "$Stopping Time"}
                }
            }
        ])
        return result.next()

    def avg_per_stop_location(self):
        result = self.db.vehicles.aggregate([
            {
                '$match': {
                    'GpsDir': {
                    '$exists': True, '$ne': None
                    }
                }
            },
            {
                '$group': {
                    '_id': {
                        'Route': "$PatternName",
                        'Stop': "$NextStopName",
                        'Long':"$GpsLong",
                        'Lat': "$GpsLat",
                        'AvgPassengersOnBoard': {'$avg':"$PassengersOnboard"},
                        'DateTime': "$GpsDate"
                    }
                }
            }
        ])
        per_route = defaultdict(list)
        for item in result:
            i = item['_id']
            per_route[i['Route']].append([i['Stop'], i['Long'], i['Lat'], i['AvgPassengersOnBoard']])
        return per_route
