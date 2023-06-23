from pymongo import MongoClient
import urllib.parse
import datetime
username = urllib.parse.quote_plus('test')
password = urllib.parse.quote_plus('Salman@2018$')

client = MongoClient("mongodb+srv://%s:%s@cluster0.wqhrr.mongodb.net/" %(username,password))

db = client.scrapy

posts = db.test_collection

post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}

post_id = posts.insert_one(post).inserted_id
print(post_id)