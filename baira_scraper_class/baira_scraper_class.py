import json
import os.path
import time
from datetime import date
import pandas as pd
import w3lib.html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from configs.config_data import WAIT, MINI_WAIT, ROOT_PATH, DATA_PATH, INFO_PATH, FILE_NAME, LINK_PATH, SITE_LINK
from functions import make_dir


class BairaScraper:
    def __init__(self, driver):
        self.wait = WAIT
        self.miniwait = MINI_WAIT
        self.driver = driver
        self.site_link = SITE_LINK
        self.file = FILE_NAME
        self.info_path = f"{ROOT_PATH}/{DATA_PATH}/{INFO_PATH}"
        self.link_path = f"{ROOT_PATH}/{DATA_PATH}/{LINK_PATH}"
        self.time = str(date.today())
        self.item = []
        self.column_names = []
        self.df = pd.DataFrame()
        self.height = int()
        self.data_list = []
        self.p_link = []
        self.run_scraper()

    def run_scraper(self):
        self.open_web_page(self.site_link)
        if not os.path.isfile(f"{self.link_path}/company_link.json"):
            self.get_company_link()
        if not os.path.isfile(f"{self.link_path}/raw_data.json"):
            self.extract_all_info()
        else:
            print("All data extracted")
        self.save_data()

    def open_web_page(self, link):
        self.driver.get(link)

    def open_link_new_tab(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

    def close_new_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def get_company_link(self):
        flag = True
        while flag:
            try:
                flag = True
                self.get_all_company_link()
                next_btn = WebDriverWait(self.driver, self.wait).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         '//div[@class="text-right"]/ul/li[13]/a'))
                )
                print(flag)
                next_btn.click()
            except:
                flag = False
                print(flag)

    def get_all_company_link(self):
        try:
            elements = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//p[@class="post-title"]/following-sibling::div/div/following-sibling::div/table/tbody/tr/td'
                     '/following-sibling::td/a'))
            )
            links = []
            for element in elements:
                link = element.get_attribute('href')
                u_dict = {'company_link': link}
                print(u_dict)
                links.append(u_dict)
                [self.p_link.append(x) for x in links if x not in self.p_link]
            make_dir(f"{self.link_path}")
            with open(f"{self.link_path}/company_link.json", 'w') as file:
                json.dump(self.p_link, file, indent=4)
        except Exception as e:
            print(f" error on get company link() - {e}")

    def extract_all_info(self):
        file = f"{self.link_path}/company_link.json"
        if os.path.isfile(file):
            with open(file, 'r') as f:
                data = json.loads(f.read())
                for item in data:
                    print(item)
                    self.open_link_new_tab(item['company_link'])
                    self.extraxt_data(link=item['company_link'])
                    self.close_new_tab()

    def extraxt_data(self, link):
        item = {}
        try:
            item["company_name"] = self.driver.find_element(By.XPATH, '//strong[text()="Name of Agency"]').click()
        except:
            item['company_name'] = "not found"

        try:
            item['company_email'] = self.driver.find_element(By.XPATH, '//td[text()="Email"]')
        except:
            item['company_email'] = "not found"

        item['source_url'] = link
        self.item.append(item)
        print(item)

    def save_data(self):
        make_dir(f"{self.info_path}")
        with open(f"{self.info_path}/{self.file}", 'w') as file:
            json.dump(self.item, file, indent=4)
