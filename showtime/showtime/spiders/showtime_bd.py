import scrapy


class ShowtimeBdSpider(scrapy.Spider):
    name = "showtime_bd"
    page_num = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = self.get_config()

    def get_config(self):
        config = {}
        config['Name'] = "showtimeBD"
        config['StartUrl'] = "http://showtimebd.com/movie/hindi_dubbed/?page=[page_num]"
        config['BaseUrl'] = "http://showtimebd.com"
        config['Recent'] = True
        config['MaxPageToCrawl'] = 48
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
            for i in response.xpath('//figure[@class="bssmall_fig"]/figcaption'):
                url = i.xpath('.//a/@href').get()
                yield response.follow(url, callback=self.parse_data)

            self.page_num += 1
            if self.page_num <= self.config['MaxPageToCrawl']:
                yield scrapy.Request(self.config['StartUrl'].replace('[page_num]', str(self.page_num)),
                                     method='GET', callback=self.parse_all)
        except Exception as e:
            print(e)

    def parse_data(self, response):
        try:
            item = {}

            date = response.xpath(
                '//i[@class="fa fa-calendar"]/following-sibling::b/following-sibling::text()').get()
            if date is not None:
                date = date.replace(':', '').strip()
            else:
                date = ''
            title = response.xpath('//div[@class="single_page"]/h1/text()').get()
            if title is not None:
                title = title
            else:
                title = ''
            views = response.xpath('//i[@class="fa fa-user"]/following-sibling::b/following-sibling::text()').get()
            if views is not None:
                views = views
            else:
                views = ''

            download = response.xpath('//button[text()="Click For Download"]/parent::a/@href').get()
            if download is not None:
                download = download
            else:
                download = download

            item['Movie_name'] = title
            item['Views'] = views
            item['Date'] = date
            item['Download_link'] = download
            item['SourceUrl'] = response.url
            yield item
        except Exception as e:
            print(e)
