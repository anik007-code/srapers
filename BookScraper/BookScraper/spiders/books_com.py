import re

import scrapy
from bs4 import BeautifulSoup


class BooksComSpider(scrapy.Spider):
    name = "books.com"
    page_num = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = self.get_config()

    def get_config(self):
        config = {}
        config["SourceKey"] = 'BooksToScrape.com'
        config['site_name'] = 'BooksToScrape.com'
        config['base_url'] = 'https://books.toscrape.com/catalogue/'
        config['StartUrl'] = 'https://books.toscrape.com/'
        return config

    def start_requests(self):
        try:
            if self.config is None:
                print(self.name, "No Config Read")
            else:
                print(self.config["SourceKey"], " Crawler Started")
                yield scrapy.FormRequest(self.config["StartUrl"], callback=self.parse_all)
        except Exception as e:
            print(self.config["SourceKey"], str(e))

    def parse_all(self, response):
        try:
            books = response.xpath('//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]')
            for single in books:
                url = single.xpath('.//article/h3/a/@href').get()
                href = self.config['base_url'] + url
                name = single.xpath('.//article/h3/a/@title').get()
                price = single.xpath('.//article/div[2]/p/text()').get()
                stock = single.xpath('.//article/div[2]/p[2]/i/following-sibling::text()').get()
                meta = {'name': name, 'price': price, 'stock':  stock}

                yield scrapy.Request(href, method='GET', meta=meta, callback=self.parse_details)

                if self.page_num < 10:
                    next_page = f'https://books.toscrape.com/catalogue/page-{self.page_num}.html'
                    self.page_num += 1
                    yield scrapy.Request(next_page, callback=self.parse_all)
        except Exception as e:
            print(f' Error in parse all- {e}')

    def parse_details(self, response):
        item = {}
        name = response.meta['name']
        if name is not None:
            item['Name'] = name.strip()
        else:
            item['Name'] = ''

        price = response.meta['price']
        if price is not None:
            item['price'] = price.strip()
        else:
            item['price'] = ''

        stock = response.meta['stock']
        if stock is not None:
            item['stock'] = stock.strip()
        else:
            item['stock'] = ''

        website_text = response.body.decode("utf-8")
        profile_soup = BeautifulSoup(website_text, "html.parser")
        profile_description = profile_soup.find('div', attrs={'id': 'content_inner'})
        if profile_description is not None:
            item['rawSummary'] = re.sub('\s+', ' ', profile_description.decode_contents())
        else:
            item['rawSummary'] = ''

        yield item