import scrapy


class EvalyComBdSpider(scrapy.Spider):
    name = "evaly.com.bd"
    page_num = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = self.get_config()

    def get_config(self):
        config = {}
        config['Name'] = "Evaly"
        config['BaseUrl'] = "https://evaly.com.bd"
        config['StartUrl'] = "https://evaly.com.bd/search?page=[page_num]"
        config['MaxPageToCrawl'] = 100
        config['Recent'] = True
        return config

    def start_requests(self):
        try:
            if self.config is not None:
                if self.config['Recent']:
                    yield scrapy.Request(self.config['StartUrl'].replace('[page_num]', str(self.page_num)),
                                         method='GET', callback=self.parse_all)
                else:
                    print("Not a valid request")
            else:
                print("No Config there")
        except Exception as e:
            print(f'Error on get request function : {e}')

    def parse_all(self, response):
        try:
            for i in response.xpath('//div[@class="bg-white border rounded-md"]'):
                url = i.xpath('.//a/@href').get()
                href = self.config['BaseUrl'] + str(url)
                title = i.xpath('.//a/div[2]/p[1]/text()').get()
                name = i.xpath('.//a/div[2]/p[2]/text()').get()
                price = i.xpath('.//a/div[2]/div/div/p[1]/text()[2]').get()
                img = i.xpath('.//a/div/div/img/@src').get()
                meta = {'name': name, 'price': price, 'title': title, 'img': img}
                yield response.follow(href, callback=self.parse_data, meta=meta)

            self.page_num += 1
            if self.page_num <= self.config['MaxPageToCrawl']:
                yield scrapy.Request(self.config['StartUrl'].replace('[page_num]', str(self.page_num)),
                                     method='GET', callback=self.parse_all)
        except Exception as e:
            print(e)

    def parse_data(self, response):
        try:
            item = {}

            name = response.meta['name']
            if name is not None:
                name = name.strip()
            else:
                name = ''

            title = response.meta['title']
            if title is not None:
                title = title.strip()
            else:
                title = ''

            price = response.meta['price']
            if price is not None:
                price = price.strip()
            else:
                price = ''

            img = response.meta['img']
            if img is not None:
                img = img.strip()
            else:
                img = ''

            item['ProductName'] = title
            item['Price'] = price
            item['CompanyName'] = name
            item['ImageLink'] = img
            item['SourceUrl'] = response.url
            yield item
        except Exception as e:
            print(e)
