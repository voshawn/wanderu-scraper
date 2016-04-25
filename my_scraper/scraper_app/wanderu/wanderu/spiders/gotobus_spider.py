from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose
from wanderu.items import BusTrip
import os
import sys
from datetime import timedelta, date


class GotobusSpider(Spider):
    name = "gotobus"
    allowed_domains = "gotobus.com"

    base_urls = [
        """http://search.gotobus.com/search/bus.do?nm=&st=0&gid=&option=Select
        &bus_from=Washington%2C+DC&bus_to=New+York%2C+NY&filter_date=""",
        """http://search.gotobus.com/search/bus.do?nm=&st=0&gid=&option=Select
        &bus_from=New+York%2C+NY&bus_to=Washington%2C+DC&filter_date="""
        ]

    constructed_urls = []

    for base_url in base_urls:
        d = date.today()
        end_date = d + timedelta(days=60)
        while d <= end_date:
            url = base_url + d.strftime("%Y-%m-%d")
            constructed_urls.append(url)
            d += timedelta(days=1)

    start_urls = constructed_urls

    trips_list_xpath = '//*[@id="listarea"]/tbody/tr[@name="table_radselect"]'
    item_fields = {
        'tripid': './/td[7]/div[@class="bus-id"]/span/text()',
        'carrier': './/td[4]/div[@class="hasicon"]/span/text()',
        'originTime': './/td[1]/text()',
        'destinationTime': './/td[3]/text()',
        'price': './/td[8]/div//strong/text()',
        # 'duration':
        # './/div[1]/div[1]/div[2]/div[3]/small/span[1]/span/text()',
        'features': './/td[6]/div/a[@data-placement ="bottom"]/@data-content',
        'soldout': './td[1]/div/@class'

    }

    def parse(self, response):
        def clean_price(x):
            return x.strip('$ \t\n\r')

        def clean_city(x):
            return x.strip(': \t\n\r')

        def clean_features(x):
            return x.replace('\t', '').replace('\n', '')

        i = 1
        for trips in Selector(response).xpath(self.trips_list_xpath):
            loader = ItemLoader(BusTrip(), selector=trips)

            loader.default_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()
            loader.price_in = MapCompose(clean_price)
            loader.originCity_in = MapCompose(clean_city)
            loader.destinationCity_in = MapCompose(clean_city)
            loader.features_in = MapCompose(clean_features)

            for field, xpath in self.item_fields.iteritems():
                loader.add_xpath(field, xpath)


            loader.add_xpath('originCity', '//*[@id="displayb'+str(i)+'_0"]/td/div/ul[1]/ul/li[1]/strong/text()')
            loader.add_xpath('originLocation', '//*[@id="displayb'+str(i)+'_0"]/td/div/ul[1]/ul/li/div[2]/a/div/text()')
            loader.add_xpath('destinationCity', '//*[@id="displayb'+str(i)+'_0"]/td/div/ul[2]/ul/li[1]/strong/text()')
            loader.add_xpath('destinationLocation', '//*[@id="displayb'+str(i)+'_0"]/td/div/ul[2]/ul/li/div[2]/a/div/text()')

            i = i + 1




            dateoftrip = str(response.url).split("=")[-1]
            loader.add_value('dateoftrip', dateoftrip.decode('unicode-escape'))
            yield loader.load_item()





