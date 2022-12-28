import time
from datetime import date
import json
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.test_config import WAIT, MINI_WAIT, ROOT_PATH, DATA_PATH, FILE_NAME, INFO_PATH, LINK_PATH
from configs.test_config import SITE_LINK
from functions import make_dir


class Test:
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

    def open_web_page(self, link):
        self.driver.get(link)

    def run_scraper(self):
        self.open_web_page(self.site_link)
        self.get_company_link()

    def open_link_new_tab(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

    def close_new_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def get_company_link(self):
        try:
            flag = True
            while flag:
                self.driver.find_element(By.XPATH, '//a[@class="number nextp"]').click()
                pages = self.driver.find_elements(By.XPATH, '//a[@class="number"]')
                page_dict = []
                cleaned_link = []
                for page in pages:
                    page = page.get_attribute('href')
                    page_dict.append(page)
                    [cleaned_link.append(x) for x in page_dict if x not in cleaned_link]
                for link in cleaned_link:
                    self.open_link_new_tab(link)
                    self.get_company_link_list()
                    self.close_new_tab()
                    print(link)
                    print("END")
        except:
            flag = False
            print(flag)

    def get_company_link_list(self):
        try:
            elements = self.driver.find_elements(By.XPATH, '//h2[@class="post-title entry-title"]/a')
            for element in elements:
                element = element.get_attribute('href')
                print(element)
        except Exception as e:
            print(f" error on get_company-link() - {e}")
