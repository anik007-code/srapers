import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.config_data import WAIT, MINI_WAIT, SITE_LINK, FILE, FILE_PATH, INFO_PATH, DATA_PATH
from functions import make_dir


class Yellowpages:
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
        self.run_scraper()

    def run_scraper(self):
        self.open_web_page()
        self.get_product_link()

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
        flag = True
        while flag:
            try:
                flag = True
                self.get_category()
                next_btn = WebDriverWait(self.driver, self.wait).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         '//li[@class="next"]/a'))
                )
                print(flag)
                next_btn.click()
            except:
                flag = False
                print(flag)

    def get_category(self):
        try:
            elements = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//div[@class="categories"]/div/div/div/a'))
            )
            for element in elements:
                link = element.get_attribute('href')
                print(link)
        except Exception as e:
            print(f"Error on 'get_category_list()' - {e}")

    def extract_data(self, link):
        item = {}
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="caption"]/h4[2]'))
            )
            item["laptop_name"] = element.text
        except:
            item["laptop_name"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="caption"]/p'))
            )
            item["description"] = element.text
        except:
            item["description"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="caption"]/h4[1]'))
            )
            item["price"] = element.text
        except:
            item["price"] = "not found"

        item["source_name"] = "TEST_SITE"
        item["URL"] = link
        self.item.append(item)

    def save_data(self):
        make_dir(f"{self.info_path}")
        with open(f"{self.info_path}/{self.file}", 'w') as file:
            json.dump(self.item, file, indent=4)
