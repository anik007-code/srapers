import re
import sys
import traceback
import scrapy
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


class PostchSpider(scrapy.Spider):
    name = "postch"
    start_urls = ['https://www.post.ch/en/jobs/jobs?jobsCategory=professionals&workload-maximum=1&workload-minimum=0']

    async def parse(self, response, **kwargs):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(response.url)

            button_selector = '//div[@class="ppm-jobs-load-more"]/button'
            link_count = 0
            while True:
                try:
                    button = await page.wait_for_selector(button_selector)
                    await button.click()
                    await page.wait_for_timeout(2000)
                    # Extract links from the current page and yield them.
                    links = await page.query_selector_all('//li[@class="ppm-jobs-list__item"]/a')
                    for link in links:
                        url = await link.get_attribute('href')
                        title = await link.evaluate(
                            '(element) => element.querySelector("h3 > span").textContent')
                        date = await link.evaluate(
                            '(element) => element.querySelector("span:nth-child(4)").textContent')
                        location = await link.evaluate(
                            '(element) => element.querySelector("span:nth-child(3)").textContent')
                        meta = {'title': title, 'date': date, 'location': location}
                        link_count += 1
                        yield scrapy.Request(url, method="GET", meta=meta, callback=self.parse_job)
                except Exception as e:
                    self.log(f"Error while clicking the 'Show More' button: {e}")
                    break
            await browser.close()
            self.log(f"Total links extracted: {link_count}")

    def parse_job(self, response):
        try:
            jobTitle = response.request.meta["title"]
            if jobTitle is not None:
                jobTitle = jobTitle.strip('/')
            else:
                jobTitle = ''
            jobLocation = response.request.meta["location"]
            if jobLocation is not None:
                jobLocation = jobLocation.strip()
            else:
                jobLocation = ''

            date = response.request.meta["date"]
            if date is not None:
                date = date
            else:
                date = ''

            website_text = response.body.decode("utf-8")
            jobs_soup = BeautifulSoup(website_text.replace("<", " <"), "html.parser")
            description = jobs_soup.find('div', {"class": "wrapper"})
            if description is not None:
                cleanContent = re.sub('\s+', ' ', description.get_text())
                rawContent = re.sub('\s+', ' ', description.decode_contents())
            else:
                cleanContent = ''
                rawContent = ''

            data_dict = {'JobTitle': jobTitle, 'JobLocation': jobLocation, 'PostedDate': date,
                         "SourceURL": response.url, 'CleanContent': cleanContent, 'RawContent': rawContent,
                         'SourceUID': response.url}

            emailList = re.findall(
                '\S+@\S+', cleanContent.strip("\n"))
            phoneList = re.findall(r'[\+\(]?[1-9][0-9 \-\(\)]{8,}[0-9]',
                                   cleanContent.strip("\n").replace('\u00a0', ' '))
            if len(emailList) > 0:
                _email = emailList[0]
                data_dict['JobContactEmails'] = _email
            if len(phoneList) > 0:
                for i in range(len(phoneList)):
                    phone = phoneList[i].strip().strip('(').strip(')')
                    if len(phone) > 0:
                        data_dict['JobContactPhone'] = phone
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
            sys.stdout.flush()

    def close(self, reason):
        try:
            print("Crawler Stopped, Total Jobs:")
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
            sys.stdout.flush()
