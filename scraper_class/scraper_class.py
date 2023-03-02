import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.config_data import WAIT, MINI_WAIT, SITE_LINK, FILE, FILE_PATH, INFO_PATH, DATA_PATH, ROOT_PATH, LINK_PATH
from functions import make_dir


class Amazon:
    def __init__(self, driver):
        self.wait = WAIT
        self.miniwait = MINI_WAIT
        self.site_link = SITE_LINK
        self.driver = driver
        self.info_path = f"{ROOT_PATH}/{DATA_PATH}/{INFO_PATH}"
        self.link_path = f"{ROOT_PATH}/{DATA_PATH}/{LINK_PATH}"
        self.file = FILE
        self.data = FILE_PATH
        self.item = []
        self.data_list = []
        self.run_scraper()

    def run_scraper(self):
        self.open_web_page()
        self.get_product_link()

    def open_new_tab(self, link):
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
                self.get_product_link_list()
                next_btn = WebDriverWait(self.driver, self.wait).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         '//a[text()="Next"]'))
                )
                print(flag)
                next_btn.click()
            except:
                flag = False
                print(flag)

    def get_product_link_list(self):
        try:
            elements = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"]/a'))
            )
            for element in elements:
                link = element.get_attribute('href')
                print(link)
                self.open_new_tab(link)
                self.extract_data(link)
                self.close_new_tab()
        except Exception as e:
            print(f"Error on 'get_category_list()' - {e}")

    def extract_data(self, link):
        item = {}
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//span[@class="a-size-large product-title-word-break"]'))
            )
            item["product_name"] = element.text
        except:
            item["product_name"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="a-section a-spacing-micro"]/span/span/span/following-sibling::span'))
            )
            item["price"] = element.text
        except:
            item["price"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//h1[text()=" About this item "]/following-sibling::ul'))
            )
            item["description"] = element.get_attribute('outerHTML')
        except:
            item["description"] = "not found"

        item["source_name"] = "AMAZON.COM"
        item["URL"] = link
        self.item.append(item)
        print(item)
        make_dir(f"{self.info_path}")
        with open(f"{self.info_path}/{self.file}", 'w') as file:
            json.dump(self.item, file, indent=4)
