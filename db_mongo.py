import pymongo


def init_db_mongo():
    client = pymongo.MongoClient('mongodb://root:example@127.0.0.1:27017/')
    database = client['crm_db']
    contacts_collection = database['contacts']
    return contacts_collection

