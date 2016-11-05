from pymongo import MongoClient
import pandas as pd


def connect_mongo(db, host='localhost', port=27017, username=None, password=None):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]

def read_mongo(db_conn, collection, query={}, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Make a query to the specific DB and Collection
    print(query)
    cursor = db_conn[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

def read_mongo_projection(db_conn, collection, query={}, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Make a query to the specific DB and Collection
    cursor = db_conn[collection].find(projection=query)

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))



    # Delete the _id
    if no_id:
        del df['_id']

    return df

def write_mongo(db_conn, collection, document):

    result = db_conn[collection].insert(document)




