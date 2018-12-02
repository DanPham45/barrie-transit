"""
Here we keep any web-DB related code
"""
import json
from datetime import datetime
from pymongo import MongoClient


class DB:

    def __init__(self, url):
        self.url = url
        self.client = MongoClient(url)
        self.db = self.client.barrieTransit

    def close(self):
        self.client.close()

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
