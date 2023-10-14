from pathlib import Path
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["file:///home/erick/tmp/sitio-web/index.html"]
    custom_settings = {
            'DEPTH_LIMIT': 3
            }


    # def start_requests(self):
    #     urls = [
    #         "https://quotes.toscrape.com/page/1/",
    #         "https://quotes.toscrape.com/page/2/"
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, depth=1):
        if depth > self.settings.getint("DEPTH_LIMIT"):
            self.log(f"🔥Reached max depth {depth} for {response.url}")
            return
        if response.headers.get("Content-Type", b"").startswith(b"text/html"):
            # depth_limit = self.settings.getint("DEPTH_LIMIT")
            self.log(f"Got successful response from {response.url} 📀  {depth}")



        # scrapy.shell.inspect_response(response, self)
        # import pudb; pudb.set_trace()
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html 🍉  {depth}"
        # Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        hrefs = response.xpath("//a/@href").extract()
        for href in hrefs:
            url = response.urljoin(href)
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(depth=depth+1))
