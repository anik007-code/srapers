import scrapy
from playwright.async_api import async_playwright


class PostchSpider(scrapy.Spider):
    name = "postch"
    start_urls = ['https://www.post.ch/en/jobs/jobs?jobsCategory=professionals&workload-maximum=1&workload-minimum=0']

    async def parse(self, response, **kwargs):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(response.url)

            # Replace 'button_selector' with the actual selector for your "Show More" button.
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
                        yield {
                            'link': await link.get_attribute('href'),

                        }
                        link_count += 1

                except Exception as e:
                    self.log(f"Error while clicking the 'Show More' button: {e}")
                    break  # Break the loop when the button is unavailable or an error occurs.

            await browser.close()
            self.log(f"Total links extracted: {link_count}")

