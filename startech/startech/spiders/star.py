import scrapy
from ..items import StartechItem


class StarSpider(scrapy.Spider):
    name = "star"
    allowed_domains = ["star.com"]
    start_urls = ["https://www.startech.com.bd/"]

    def parse(self, response, **kwargs):
        for link in (response.xpath('//div[@class="cat-item"]/a').css('::attr(href)').extract()):
            yield response.follow(link, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        for link in (response.xpath('//h4[@class="p-item-name"]/a').css('::attr(href)').extract()):
            yield response.follow(link, callback=self.main_item, dont_filter=True)

        next_page = response.xpath('//a[text()="NEXT"]').css('::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_item, dont_filter=True)

    def main_item(self, response):
        item = StartechItem()
        name = response.xpath('//h1[@class="product-name"]').css('::text').extract()
        item['name'] = name
        yield item
