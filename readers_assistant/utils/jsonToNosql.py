from pymongo import MongoClient
import json
from bson.son import SON

myclient = MongoClient("mongodb://localhost:27017/")
db = myclient['jmdict']
collection = db['word_collection']
collection.drop()

# with open('data.json') as file:
#     file_data = json.load(file)

# words = file_data['JMdict']['entry']
# for word in words:
#     collection.insert_one(word)

# r = collection.find({ "ent_seq": "1000810"})

# list(map(print, r['k_ele']))
# cursor = db.inventory.find({"k_ele": SON([("keb", "いじり回す")])})
# list(map(print, cursor))
# print(r['k_ele'])
