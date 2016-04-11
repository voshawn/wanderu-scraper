# import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import XPathItemLoader
from scrapy.loader.processors import Join, MapCompose
from wanderu.items import BusTrip
# from selenium import webdriver


class WanderuSpider(Spider):
    name = "wanderu"
    allowed_domains = "wanderu.com"
    start_urls = ["https://www.wanderu.com/en/depart/Washington%2C%20DC%2C%20USA/New%20York%2C%20NY%2C%20USA/2016-04-11"]

    trips_list_xpath = '//div[@class="trip-item"]'
    item_fields = {
        'tripid': './/@id',
        'carrier': './/div/div/div/div/div/@data-original-title'

    }

    def parse(self, response):

        for trips in Selector(text=response.body).xpath(self.trips_list_xpath):
            loader = XPathItemLoader(BusTrip(), selector=trips)

            loader.default_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()

            for field, xpath in self.item_fields.iteritems():
                loader.add_xpath(field, xpath)
            yield loader.load_item()

    # def __init__(self):
    #     self.driver = webdriver.Firefox()

    # def parse(self, response):
    #         self.driver.get('https://www.example.org/abc')

    #         while True:
    #             try:
    #                 next = self.driver.find_element_by_xpath('//*[@id="BTN_NEXT"]')
    #                 url = 'http://www.example.org/abcd'
    #                 yield scrapy.Request(url, callback=self.parse2)
    #                 next.click()
    #             except:
    #                 break

    #         self.driver.close()

    # def parse2(self, response):
    #     print 'you are here!'
