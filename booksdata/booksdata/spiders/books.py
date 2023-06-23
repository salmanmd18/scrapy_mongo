import scrapy
from pathlib import Path
from pymongo import MongoClient
import urllib.parse
import datetime

username = urllib.parse.quote_plus('test')
password = urllib.parse.quote_plus('Salman@2018$')

client = MongoClient("mongodb+srv://%s:%s@cluster0.wqhrr.mongodb.net/" %(username,password))

db = client.scrapy


def insertToDb(page,title,rating,image,price,inStock):
    collection = db[page]
    doc = {
        "title" : title,
        "rating" : rating,
        "image" : image,
        "price" : price,
        "inStock" : inStock,
        "date" : datetime.datetime.now(tz=datetime.timezone.utc)
    }
    inserted = collection.insert_one(doc)
    return inserted.inserted_id
class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["to.scrape.com"]
    start_urls = ["https://to.scrape.com"]

    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-2]
        filename  = f"books-{page}.html"
        bookdetail = {}
        #save the content as files
        # Path(filename).write_bytes(response.body)
        self.log(f"saved file {filename}")
        # a = response.css(".product_pod")
        # # print(a)
        # b = a.css("a")
        # print(b)
        cards = response.css(".product_pod")
        for card in cards:
            title = card.css("h3>a::text").get()
            # print(title)
            rating = card.css(".star-rating").attrib["class"].split(" ")[1]
            # print(rating)
            image = card.css(".image_container img")
            image = image.attrib["src"].replace("../../../../media","https://books.toscrape.com/media")
            # print(image)

            price = card.css(".price_color::text").get()
            # print(price[1:])

            availability = card.css(".availability")

            if len(availability.css(".icon-ok")) > 0:
                inStock = True
            else:
                inStock = False
            insertToDb(page,title,rating,image,price,inStock)    