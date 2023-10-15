# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from bs4 import BeautifulSoup
from itemloaders.processors import MapCompose, TakeFirst
import re


def extract_text(html):
    soup = BeautifulSoup(html, "html.parser").get_text().strip()
    return set(re.split(r"[^a-zA-Z0-9]+", soup))


class RobotoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field(
            output_processor = TakeFirst()
            )
    content = scrapy.Field(
            output_processor = MapCompose(extract_text)
            )
    depth = scrapy.Field(
            output_processor = TakeFirst()
            )
