from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose
from wanderu.items import BusTrip
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import sys
from datetime import timedelta, date
from xvfbwrapper import Xvfb
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class WanderuSpider(Spider):
    name = "wanderu"
    allowed_domains = "wanderu.com"

    base_urls = [
        """https://www.wanderu.com/en/depart/New%20York%2C%20NY%2C%20USA/
        Washington%2C%20DC%2C%20USA/""",
        """https://www.wanderu.com/en/depart/Washington%2C%20DC%2C%20USA/
        New%20York%2C%20NY%2C%20USA/"""
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

    trips_list_xpath = '//div[@class="trip-item"]'
    item_fields = {
        'tripid': '(.//@id)[1]',
        'carrier': './/div[1]/div[1]/div[2]/div[1]/div/@data-original-title',
        'originTime': './/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]/text()',
        'originCity': './/div[1]/div[1]/div[1]/div[1]/div[1]/span[2]/text()',
        'originLocation': './/div[1]/div[1]/div[1]/div[1]/div[2]/span/text()',
        'destinationTime':
        './/div[1]/div[1]/div[1]/div[2]/div[1]/span[1]/text()',
        'destinationCity':
        './/div[1]/div[1]/div[1]/div[2]/div[1]/span[2]/text()',
        'destinationLocation':
        './/div[1]/div[1]/div[1]/div[2]/div[2]/span/text()',
        'price': './/div[1]/div[1]/div[1]/div[3]/span/text()',
        'duration':
        './/div[1]/div[1]/div[2]/div[3]/small/span[1]/span/text()',
        'features':
        './/div[1]/div[1]/div[2]/div[2]/div/div/@data-original-title'

    }

    def __init__(self):
        self.vdisplay = Xvfb()
        chromedriver = os.path.join(os.path.dirname(__file__), "chromedriver")
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)
        dispatcher.connect(self.close, signals.spider_closed)
        self.vdisplay.start()

    def close(self, spider):
        self.driver.quit()
        self.vdisplay.stop()

    def parse(self, response):
        self.driver.get(response.url)
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                        '//*[@id="depart-container"]/div[2]/div[1]/div/[@style="width: 0%;"]')))
        except TimeoutException:
            print 'Page load time out'
            pass

        while True:
            try:
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                                '//*[@id="depart-container"]/div/div/div/button')))
                except TimeoutException:
                    break

                next = self.driver.find_element_by_xpath(
                    '//*[@id="depart-container"]/div/div/div/button')
                next.click()

            except ElementNotVisibleException:
                break
        for trips in Selector(
                text=self.driver.page_source).xpath(self.trips_list_xpath):
            loader = ItemLoader(BusTrip(), selector=trips)

            loader.default_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()

            for field, xpath in self.item_fields.iteritems():
                loader.add_xpath(field, xpath)
            dateoftrip = str(response.url).split("/")[-1]
            loader.add_value('dateoftrip', dateoftrip.decode('unicode-escape'))
            yield loader.load_item()



