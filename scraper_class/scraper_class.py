import json
from datetime import date
import pandas as pd
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from configs.config_credentials import USER_NAME, PASSWORD, UNIVERSITY
from configs.config_data import WAIT, MINI_WAIT, ROOT_PATH, DATA_PATH, INFO_PATH, \
    LINK_PATH, FILE, LINKS, IMAGE_PATH
import time
from functions import make_dir, image_downloader


class Linkedin:
    def __init__(self, driver):
        self.wait = WAIT
        self.miniwait = MINI_WAIT
        self.site_link = LINKS
        self.driver = driver
        self.uni = UNIVERSITY
        self.user_name = USER_NAME
        self.password = PASSWORD
        self.file = FILE
        self.info_path = f"{ROOT_PATH}/{DATA_PATH}/{INFO_PATH}"
        self.link_path = f"{ROOT_PATH}/{DATA_PATH}/{LINK_PATH}"
        self.img_path = f"{ROOT_PATH}/{DATA_PATH}/{IMAGE_PATH}"
        self.image_path = IMAGE_PATH
        self.time = str(date.today())
        self.item = []
        self.column_names = []
        self.df = pd.DataFrame()
        self.data_list = []
        self.people = []
        self.company_link = []
        self.run_scraper()

    def run_scraper(self):
        self.open_web_page(self.site_link)
        self.log_in()
        self.search_uni()
        self.people_link()
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

    def log_in(self):
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//input[@id="session_key"]')))
            element.click()
            element.clear()
            element.send_keys(self.user_name)
        except Exception as e:
            print(f" error log in {e}")
        time.sleep(2)
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//input[@autocomplete="current-password"]')))
            element.click()
            element.clear()
            element.send_keys(self.password)
        except:
            print("Not found ")

        try:
            WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//button[@class="sign-in-form__submit-button"]'))).click()
        except:
            print("Not found ")

    def search_uni(self):
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@id="global-nav-typeahead"]/input')))
            element.click()
            element.clear()
            element.send_keys(self.uni)
            element.send_keys(Keys.RETURN)
            time.sleep(5)
        except Exception as e:
            print(f" error on {e}")
        time.sleep(5)
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//span[@class="entity-result__title-line entity-result__title-line--2-lines pt1"]/span/a')))
            element.click()
            time.sleep(5)
        except Exception as e:
            print(f" error on {e}")
        time.sleep(5)
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//span[@class="org-top-card-secondary-content__see-all t-normal t-black--light '
                     'link-without-visited-state link-without-hover-state"]')))
            element.click()
            time.sleep(5)
        except Exception as e:
            print(f" error on {e}")

    def people_link(self):
        try:
            while True:
                self.people_link_list()
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                flag = True
                while flag:
                    try:
                        flag = True
                        btn = WebDriverWait(self.driver, self.miniwait).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                 '//div[@class="artdeco-pagination__page-state"]/following-sibling::button')))
                        btn.click()
                    except:
                        flag = False
                        print(f"{flag}")
        except Exception as e:
            print(f" error- {e}")

    def people_link_list(self):
        try:
            elements = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//div[@class="mb1"]/div/div/span/span/a')))
            for element in elements:
                link = element.get_attribute('href')
                self.people.append(link)
                self.open_link_new_tab(link)
                self.extract_data(link)
                self.close_new_tab()

        except Exception as e:
            print(f" error on {e}")

    def extract_data(self, link):
        item = {}
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]')))
            item['name'] = element.text
        except:
            item['name'] = "not found"
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="text-body-medium break-words"]')))
            item['profession'] = element.text
        except:
            item['profession'] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//span[@class="t-black--light"]/span')))
            item['total_connection'] = element.text
        except:
            item['total_connection'] = "not found"

        try:
            elements = self.driver.find_element(By.XPATH, '//img[@class="pv-top-card-profile-picture__image '
                                                          'pv-top-card-profile-picture__image--show '
                                                          'ember-view"]').get_attribute('src')
            image_downloader(elements, item['name'], self.img_path)
        except Exception as e:
            print(f" error found in saving images {e}")

        item['source_URL'] = link
        item['source_name'] = "LinkedIn"

        self.item.append(item)
        print(item)

    def save_data(self):
        make_dir(f"{self.info_path}")
        with open(f"{self.info_path}/{self.file}", 'w') as file:
            json.dump(self.item, file, indent=4)
