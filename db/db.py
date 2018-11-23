"""
Here we keep any web-DB related code
"""
import json
from datetime import datetime
from pymongo import MongoClient


class DB:

    def __init__(self, url):
        self.url = url
        client = MongoClient(url)
        self.db = client.barrie_bus

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
        return {'routes': self.db.routes.find().distinct('RouteShortName')}

    def get_location_by_name(self):
        locations = self.db.vehicles.find(
            {'PatternName':{'$exists':True}},
            {'PatternName':1,'GpsDate':1,'GpsLong':1, 'GpsLat':1, '_id':0}
        )
        loc_list = [loc for loc in locations]
        return (loc_list)
