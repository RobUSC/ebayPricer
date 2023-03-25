from pymongo import MongoClient
from bson import ObjectId

from ebayPricer import constants

# CONNECTION_STRING= 'mongodb://ebayPricer:4a!t1AIadUc&6!al@ebayPricer-026603657099.us-east-1.docdb-elastic.amazonaws.com:27017'
CONNECTION_STRING = 'mongodb://localhost:27017'
client = MongoClient(CONNECTION_STRING)
database = client['EbayPricer']
item_list_collection = database['items']
file_import_collection = database['file_import']
line_delimiter = '+++++++++++++++++++++++++++++++++++++++++++++++++++'
noisy = True


def get_item_list_from_db(list_id):
    return item_list_collection.find_one(list_id)


def get_item_lists_from_db(query):
    return item_list_collection.find(query)


def add_item_list_record(query):
    inserted = item_list_collection.insert_one(query)
    return inserted.inserted_id


def add_item_list_records(query):
    inserted = item_list_collection.insert_many(query)
    return inserted.inserted_ids


def update_item_list_record(item):
    item_list_collection.replace_one(filter={'_id': ObjectId(item['_id'])},
                                     replacement=item,
                                     upsert=True)


def remove_item_list_record(query):
    return item_list_collection.delete_one(query)


def remove_item_list_records(query):
    return item_list_collection.delete_many(query)


def clear_file_imports():
    item_list_collection.delete_many({})
    file_import_collection.delete_many({})

def add_file_import(query):
    one = file_import_collection.find_one(query)
    if one is None:
        file_import_collection.insert_one(query)
        return True
    return False

def printer(msg):
    if noisy:
        print(msg)


def test_db_functions(data_setup, clean_up):
    printer('Database Names %s' % client.list_database_names())
    printer('Collection Names %s' % database.list_collection_names())
    if clean_up:
        var = remove_item_list_records({})
        printer('Clean up deleted %s record(s)' % var.deleted_count)
    if bool(data_setup):
        printer(line_delimiter)
        created_list = add_item_list_records(constants.item_list)
        printer('Inserted %s records from %s' % (len(created_list), constants.item_list))
        printer(line_delimiter)
        var = get_item_lists_from_db({'publisher': 'Marvel'})
        printer('Fetched many records')
        for item in var:
            printer(item)
        printer(line_delimiter)
        printer('Fetched all records')
        var = get_item_lists_from_db(None)
        for item in var:
            printer(item)
        printer(line_delimiter)


# noisy = False
# test_db_functions(True, True)
