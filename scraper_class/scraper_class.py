import json
import time
from selenium.webdriver.common.by import By
from configs.config_data import WAIT, MINI_WAIT, SITE_LINK, FILE, FILE_PATH, INFO_PATH, DATA_PATH
from functions import make_dir


class Goku:
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
        self.click()
        self.get_movie_link()
        self.sava_data()

    def open_link_new_tab(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

    def close_new_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def open_web_page(self):
        self.driver.get(self.site_link)

    def click(self):
        try:
            tv = self.driver.find_element(By.XPATH, '//ul[@class="top-menu-nav"]/li[5]/a')
            tv.click()
        except:
            print("Not found Tv Series")

    def get_movie_link(self):
        flag = True
        while flag:
            try:
                flag = True
                self.get_movie_link_list()
                btn = self.driver.find_element(By.XPATH, '//a[@title="Next"]')
                btn.click()
            except:
                flag = False
                print(flag)

    def get_movie_link_list(self):
        try:
            elements = self.driver.find_elements(By.XPATH, '//a[@class="movie-link"]')
            links = []
            for element in elements:
                url = element.get_attribute('href')
                links.append(url)
            for link in links:
                self.open_link_new_tab(link)
                self.extract_data()
                self.close_new_tab()
        except Exception as e:
            print(f" error on {e}")

    def extract_data(self):
        item = {}
        try:
            item['movie_name'] = self.driver.find_element(By.XPATH, '//div[@class="is-name"]/h3').text
        except:
            item['movie_name'] = "not found"
        try:
            item['movie_description'] = self.driver.find_element(By.XPATH, '//div[@class="is-description"]//div['
                                                                           '@class="text-cut"]').text
        except:
            item['movie_description'] = "not found"
        try:
            item['movie_genres'] = self.driver.find_element(By.XPATH, '//div[@class="value"]/a').text
        except:
            item['movie_genres'] = "not found"
        try:
            item['cast'] = self.driver.find_element(By.XPATH, '//div[text()="Cast:"]/following-sibling::div').text
        except:
            item['cast'] = "not found"
        try:
            item['country'] = self.driver.find_element(By.XPATH, '//div[text()="Country:"]/following-sibling::div').text
        except:
            item['country'] = "not found"
        try:
            item['duration'] = self.driver.find_element(By.XPATH, '//div[text()="Duration:"]/following-sibling::div').text
        except:
            item['duration'] = "not found"
        item["source_name"] = "GOKU.TO"
        self.item.append(item)
        print(item)

    def sava_data(self):
        make_dir(f"{self.info_path}")
        with open(f"{self.info_path}/{self.file}", 'w') as file:
            json.dump(self.item, file, indent=4)
