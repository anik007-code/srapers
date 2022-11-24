import json
import time
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.config_data import WAIT, MINI_WAIT, SITE_LINK, FILE, FILE_PATH
from functions import make_dir


class TechnicalInstituteScraper:
    def __init__(self, driver, info_path):
        self.wait = WAIT
        self.miniwait = MINI_WAIT
        self.site_link = SITE_LINK
        self.driver = driver
        self.info_path = info_path
        self.file = FILE
        self.data = FILE_PATH
        self.item = []
        self.data_list = []
        self.run_scraper()

    def run_scraper(self):
        self.open_web_page()
        self.save_data()
        self.get_institute_link()

    def open_web_page(self):
        self.driver.get(self.site_link)

    def get_institute_link(self):
        flag = True
        while flag:
            try:
                flag = True
                self.get_institute_link_list()
                next_btn = WebDriverWait(self.driver, self.wait).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         '//a[@class="nextLink"]'))
                )
                print(flag)
                next_btn.click()
            except:
                flag = False
                print(flag)
                self.get_institute_link_list()

    def get_institute_link_list(self):
        try:
            elements = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//div[@id="list-competencyStandardUpload"]/div/div/table/tbody/tr/td/a'))
            )
            for element in elements:
                link = element.get_attribute('href')
                print(link)
                self.open_link_new_tab(link)
                self.extract_data()
                self.close_new_tab()

        except Exception as e:
            print(f"Error on 'get_category_list()' - {e}")

    def open_link_new_tab(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

    def close_new_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def extract_data(self):
        item = {}
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//ol[@class="property-list instituteAccreditation"]/table/tbody/tr[1]/td/span'))
            )
            item["institute_code"] = element.text
        except:
            item["institute_code"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//ol[@class="property-list instituteAccreditation"]/table/tbody/tr[2]/td/span'))
            )
            item["institute_email"] = element.text
        except:
            item["institute_email"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//ol[@class="property-list instituteAccreditation"]/table/tbody/tr[3]/td/span'))
            )
            item["institute_division"] = element.text
        except:
            item["institute_division"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//ol[@class="property-list instituteAccreditation"]/table/tbody/tr[4]/td/span'))
            )
            item["institute_upazila"] = element.text
        except:
            item["institute_upazila"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//ol[@class="property-list instituteAccreditation"]/table/tbody/tr[5]/td/span'))
            )
            item["post_office"] = element.text
        except:
            item["post_office"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//ol[@class="property-list instituteAccreditation"]/table/tbody/tr[6]/td/span'))
            )
            item["institute_name"] = element.text
        except:
            item["institute_name"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//ol[@class="property-list instituteAccreditation"]/table/tbody/tr[7]/td/span'))
            )
            item["institute_postal_address"] = element.text
        except:
            item["institute_postal_address"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//ol[@class="property-list instituteAccreditation"]/table/tbody/tr[9]/td/span'))
            )
            item["institute_responder_name"] = element.text
        except:
            item["institute_responder_name"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//ol[@class="property-list instituteAccreditation"]/table/tbody/tr[11]/td/span'))
            )
            item["institute_accrediation_year"] = element.text
        except:
            item["institute_accrediation_year"] = "not found"
        self.item.append(item)

    def save_data(self):
        make_dir(f"{self.info_path}")
        with open(f"{self.info_path}/{self.file}", 'w') as file:
            json.dump(self.item, file, indent=4)