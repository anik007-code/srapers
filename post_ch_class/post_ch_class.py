import json
import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.config_data import WAIT, MINI_WAIT, SITE_LINK, FILE, FILE_PATH, INFO_PATH, DATA_PATH
from functions import make_dir


class PostScraper:
    def __init__(self, driver):
        self.wait = WAIT
        self.miniwait = MINI_WAIT
        self.site_link = SITE_LINK
        self.driver = driver
        self.info_path = INFO_PATH
        self.data_path = DATA_PATH
        self.file = FILE
        self.data = FILE_PATH
        self.item = []
        self.data_list = []
        self.time_limit = 180
        self.run_scraper()

    def run_scraper(self):
        self.open_web_page()
        # start_time = time.time()  # Record the start time
        self.get_product_link()
        # end_time = time.time()  # Record the end time
        # elapsed_time = end_time - start_time
        # if elapsed_time > self.time_limit:
        #     print(f"Time limit of {self.time_limit} seconds reached.")
        # else:
        #     print(f"Function completed within {elapsed_time} seconds.")
        self.extract_all()
        self.save_data()

    def open_link_new_tab(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

    def close_new_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def open_web_page(self):
        self.driver.get(self.site_link)

    def get_product_link(self):
        start_time = time.time()  # Record the start time
        flag = True
        while flag:
            if time.time() - start_time >= self.time_limit:
                print(f"Time limit of {self.time_limit} seconds reached.")
                break

            try:
                self.get_product_link_list()
                show_more = WebDriverWait(self.driver, self.wait).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//div[@class="ppm-jobs-load-more"]/button'))
                )
                self.driver.execute_script("arguments[0].click();", show_more)
            except:
                flag = False
        print(flag)  # Print the final value of flag after the loop

    def get_product_link_list(self):
        try:
            elements = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//li[@class="ppm-jobs-list__item"]/a'))
            )
            job_links = []
            for element in elements:
                link = element.get_attribute('href')
                # print(link)
                job_links.append(link)
            [self.item.append(x) for x in job_links if x not in self.item]
            make_dir(f'{self.info_path}')
            with open(f'{self.info_path}/links.json', 'w') as file:
                json.dump(self.item, file, indent=4)
        except Exception as e:
            print(f"Error on 'get_category_list()' - {e}")

    def extract_all(self):
        try:
            for item in self.item:
                self.open_link_new_tab(item)
                self.extract_data(item)
                self.close_new_tab()
        except:
            print('Not extracting')

    def extract_data(self, link):
        item = {}

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     './/h1'))
            )
            item["title"] = element.text
        except:
            item["title"] = "not found"

        # website_text = response.body.decode("latin-1") #used in Scrapy.
        website_text = self.driver.page_source
        jobs_soup = BeautifulSoup(website_text.replace("<", " <"), "html.parser")

        description = jobs_soup.find('div', {"class": "wrapper"})
        if description is not None:
            item['cleanContent'] = re.sub('\s+', ' ', description.get_text())
            item['rawContent'] = re.sub('\s+', ' ', description.decode_contents())
        else:
            item['cleanContent'] = 'not found'
            item['rawContent'] = ''

        emailList = re.findall(
            '\S+@\S+', item['cleanContent'].strip("\n"))
        phoneList = re.findall(r'[\+\(]?[1-9][0-9 \-\(\)]{8,}[0-9]', item['cleanContent'].strip("\n").replace('\u00a0', ' '))
        if len(emailList) > 0:
            _email = emailList[0]
            item['Email'] = _email
        if len(phoneList) > 0:
            for i in range(len(phoneList)):
                phone = phoneList[i].strip().strip('(').strip(')')
                if len(phone) > 0:
                    item['Phone'] = phone
        item["source_name"] = "Post.ch"
        item["URL"] = link
        self.data_list.append(item)
        print(item)

    def save_data(self):
        make_dir(f"{self.info_path}")
        with open(f"{self.info_path}/{self.file}", 'w') as file:
            json.dump(self.data_list, file, indent=4)
