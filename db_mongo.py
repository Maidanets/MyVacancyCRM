import pymongo
import os

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')


def init_db_mongo():
    client = pymongo.MongoClient(f'mongodb://root:example@{MONGO_HOST}:27017/')
    database = client['crm_db']
    contacts_collection = database['contacts']
    return contacts_collection

