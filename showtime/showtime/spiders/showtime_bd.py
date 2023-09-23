import json

import scrapy
from ..items import ShowtimeItem


class ShowtimeBdSpider(scrapy.Spider):
    name = "showtime_bd"
    page_number = 1
    start_urls = ["http://showtimebd.com/movie/hindi_dubbed"]

    def parse(self, response, **kwargs):
        item = ShowtimeItem()
        title = response.css('figcaption > a::text').extract()
        views = response.css('#contentSection p::text').extract()

        item["title"] = title
        item['views'] = views

        yield item

        next_page = f'http://showtimebd.com/movie/hindi_dubbed/?page={self.page_number}'
        if self.page_number <= 42:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)

