import os
import pymongo


client = pymongo.MongoClient(host=os.environ['MONGO_HOST'], port=27017)
db = client.nashenas_telegram_bot
