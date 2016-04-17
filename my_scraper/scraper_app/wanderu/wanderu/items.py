# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class BusTrip(Item):
    tripid = Field()
    carrier = Field()
    originTime = Field()
    originCity = Field()
    originLocation = Field()
    destinationTime = Field()
    destinationCity = Field()
    destinationLocation = Field()
    price = Field()
    duration = Field()
    features = Field()
    dateoftrip = Field()

