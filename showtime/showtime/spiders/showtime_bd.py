import time

import scrapy
from ..items import ShowtimeItem


class ShowtimeBdSpider(scrapy.Spider):
    name = "showtime_bd"
    page_number = 1
    start_urls = ["http://showtimebd.com/movie/hindi_dubbed"]
    custom_settings = {
        'FEEDS': {
            'moviedata.json': {'format': 'json', 'overwrite': True},
        }
    }

    def parse(self, response, **kwargs):
        for i in response.xpath('//figure[@class="bssmall_fig"]/figcaption'):
            url = i.xpath('.//a/@href').get()
            yield response.follow(url, callback=self.parse_all)

        next_page = f'http://showtimebd.com/movie/hindi_dubbed/?page={self.page_number}'
        if self.page_number <= 42:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_all(self, response):
        item = ShowtimeItem()
        title = response.xpath('//div[@class="single_page"]/h1/text()').get()
        pub_date = response.xpath('//i[@class="fa fa-calendar"]/following-sibling::b/following-sibling::text()').get()
        views = response.xpath('//i[@class="fa fa-user"]/following-sibling::b/following-sibling::text()').get()
        if pub_date is not None:
            # pub_date = pub_date.strip()
            pub_date = pub_date.replace(':', '').strip()
        item["title"] = title
        item['pub_date'] = pub_date
        item['views'] = views

        yield item
