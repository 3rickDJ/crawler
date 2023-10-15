from pathlib import Path
import scrapy
from scrapy.loader import ItemLoader
from roboto.items import RobotoItem
from scrapy.exceptions import CloseSpider


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://localhost:8080/"]
    custom_settings = {
            'DEPTH_LIMIT': 3
            }

    def parse(self, response, depth=1):
        # if is a html page save it
        if response.headers.get("Content-Type", b"").startswith(b"text/html"):
            l = ItemLoader(item=RobotoItem(), response=response)
            l.add_value("url", response.url)
            l.add_value("content", response.text)
            l.add_value("depth", depth)
            item = l.load_item()
            self.log(f"Got successful response from {response.url} 📀  {depth}")
            yield item
            # depth_limit = self.settings.getint("DEPTH_LIMIT")



        # scrapy.shell.inspect_response(response, self)
        # import pudb; pudb.set_trace()
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html 🍉  {depth}"
        # Path(filename).write_bytes(response.body)H
        self.log(f"Saved file {filename}")
        hrefs = response.xpath("//a/@href").extract()
        for href in hrefs:
            url = response.urljoin(href)
            if depth >= self.settings.getint("DEPTH_LIMIT"):
                yield scrapy.Request(url=url, callback=self.parse_last)
            else:
                yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(depth=depth+1))

    def parse_last(self, response):
        if response.headers.get("Content-Type", b"").startswith(b"text/html"):
            max_depth = self.settings.getint("DEPTH_LIMIT")
            l = ItemLoader(item=RobotoItem(), response=response)
            l.add_value("url", response.url)
            l.add_value("content", response.text)
            l.add_value("depth", max_depth)
            self.log(f"Got successful response from {response.url} 📀  {max_depth}")
            item = l.load_item()
            yield item
