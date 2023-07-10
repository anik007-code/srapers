import json
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.config_data import WAIT, MINI_WAIT, SITE_LINK, FILE, FILE_PATH, INFO_PATH, DATA_PATH, ROOT_PATH, LINK_PATH
from functions import make_dir


class DaadScraper:
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
        self.product = []
        self.data_list = []
        self.run_scraper()

    def run_scraper(self):
        self.open_web_page()
        self.click_on_add()
        self.get_university_list()
        self.get_university_link_list()
        # self.save_data()

    def open_link_new_tab(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

    def close_new_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def open_web_page(self):
        self.driver.get(self.site_link)

    def click_on_add(self):
        try:
            accept = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//button[text()="Accept all cookies"]'))
            )
            accept.click()
        except Exception as e:
            print(f"Adds not found {e}")

    def get_university_list(self):
        try:
            flag = True
            while flag:
                action = ActionChains(self.driver)
                self.get_university_link_list()
                next_btn = WebDriverWait(self.driver, self.wait).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         '//div[@class="c-result-pagination__links d-inline ml-2"]/a[2]'))
                )
                print(flag)
                # self.driver.execute_script("arguments[0].scrollIntoView();", next_btn)
                # next_btn.click()
                # self.driver.execute_script("arguments[0].click();", next_btn)
                action.move_to_element(next_btn).click().perform()
                time.sleep(5)
        except:
            flag = False
            print(f"Error is {flag}")

    def get_university_link_list(self):
        try:
            elements = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//a[@class="list-inline-item mr-0 js-course-detail-link"]'))
            )
            links = []
            for element in elements:
                link = element.get_attribute('href')
                print(link)
                self.product.append(link)
            make_dir(f"{self.link_path}")
            with open(f"{self.link_path}/links.json", 'w') as file:
                json.dump(self.product, file, indent=4)
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
