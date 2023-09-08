import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response, **kwargs):
        title = response.css('title::text').extract()
        quotes = response.css('span.text::text').extract()
        author = response.css('small::text').extract()
        author_details = response.css('a::text').extract()
        tags = response.css('div.tags a::text').extract()
        yield {"Title": title,
               "Quotes": quotes,
               "Author": author,
               "Author_details": author_details,
               "Tags": tags}
