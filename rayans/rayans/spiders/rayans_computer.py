import re
import scrapy
from bs4 import BeautifulSoup
from ..items import RayansItem
from urllib.parse import urlencode

API_KEY = '51e43be283e4db2a5afb62660xxxxxx'


def get_scraperapi_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class RayansComputerSpider(scrapy.Spider):
    name = "rayans_computer"
    start_urls = ["https://www.ryanscomputers.com/categories"]

    def parse(self, response, **kwargs):
        for link in (response.xpath('//a[@class="nav-link text-dark fw-bold"]').css('::attr(href)').extract()):
            yield response.follow(link, callback=self.parse_subcategory, dont_filter=True)

    def parse_subcategory(self, response):
        for product_links in (response.xpath('//p[@class="card-text p-0 m-0"]/a').css('::attr(href)').extract()):
            # yield response.follow(product_links, callback=self.parse_extract)
            yield response.follow(product_links, dont_filter=True)

        next_page = (response.xpath('//a[@aria-label="Next »"]').css('::attr(href)').get())
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_subcategory, dont_filter=True)

    def main_page(self, response):
        item = RayansItem()

        Title = response.xpath('//h1[@itemprop="name"]/text()').extract()
        title = self.cleanText(self.parseText(self.listToStr(Title)))
        item['title'] = title
        yield item

    # # Methods to clean and format text to make it easier to work with later
    def listToStr(self, MyList):
        dumm = ""
        MyList = [i.encode('utf-8') for i in MyList]
        for i in MyList: dumm = "{0}{1}".format(dumm, i)
        return dumm

    def parseText(self, str):
        soup = BeautifulSoup(str, 'html.parser')
        return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0", ' ', soup.get_text()).strip()

    def cleanText(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()
        text = re.sub("( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+", ' ', text).strip()
        return text
