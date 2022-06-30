from logging import raiseExceptions
from pymongo import MongoClient
from app_utils import MONGODB_COLLECTION_NAME, MONGODB_NAME, MONGODB_URI_ADMIN, MONGODB_URI_USER


def registerLinkUser(userid, serverLink):
    '''
    Adds a serverLink in the links collection of user-db in MongoDB.

    args: userid: str, serverLink: str

    return: None
    '''
    client = MongoClient(MONGODB_URI_ADMIN) 
    db = client[MONGODB_NAME]
    collection = db[MONGODB_COLLECTION_NAME]

    try:
        collection.update_one({'userid': userid}, {'$addToSet': {'links': serverLink}}, upsert=True)
    except Exception as err:
            raiseExceptions(err)    