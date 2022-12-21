import time
from datetime import date
import json
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.config_data import SITE_LINK, WAIT, MINI_WAIT, ROOT_PATH, DATA_PATH, FILE_NAME, INFO_PATH, LINK_PATH
from functions import make_dir


class BkmeaScraper:
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
        flag = True
        while flag:
            self.get_company_link()
        self.save_to_json()

    def oepn_link_new_tab(self, link):
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
                self.get_company_link_list()
                next_btn = WebDriverWait(self.driver, self.wait).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         '//i[@class="el-icon el-icon-arrow-right"]'))
                )
                print(flag)
                next_btn.click()
            except:
                flag = False
                print(flag)

    def get_company_link_list(self):
        try:
            elements = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr/td[5]/div/a'))
            )
            for element in elements:
                link = element.get_attribute('href')
                print(link)
                self.oepn_link_new_tab(link)
                self.extract_information(link)
                self.close_new_tab()
        except Exception as e:
            print(f"Error on 'click_on_sign_in() next_button' - {e}")

    def extract_information(self, link):
        item = {}
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][1]/table/tbody/tr/th[text()="Company '
                     'Name"]/following-sibling::td'))
            )
            item["company_name"] = element.text
        except:
            item["company_name"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][1]/table/tbody/tr/th[text()="BKMEA Membership '
                     'Number"]/following-sibling::td'))
            )
            item["bkmea_reg_number"] = element.text
        except:
            item["bkmea_reg_number"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][1]/table/tbody/tr/th[text()="Membership '
                     'Type"]/following-sibling::td'))
            )
            item["membership_type"] = element.text
        except:
            item["membership_type"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][1]/table/tbody/tr/th[text()="Membership '
                     'Category"]/following-sibling::td'))
            )
            item["membership_category"] = element.text
        except:
            item["membership_category"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][1]/table/tbody/tr/th[text()="Registration '
                     'Date"]/following-sibling::td'))
            )
            item["registration_date"] = element.text
        except:
            item["registration_date"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][1]/table/tbody/tr/th[text()="Location"]/following-sibling::td'))
            )
            item["location"] = element.text
        except:
            item["location"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][2]/table/tbody/tr/th[text()="Name"]/following-sibling::td'))
            )
            item["dir_name"] = element.text
        except:
            item["dir_name"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][2]/table/tbody/tr/th[text('
                     ')="Designation"]/following-sibling::td'))
            )
            item["dir_designation"] = element.text
        except:
            item["dir_designation"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][2]/table/tbody/tr/th[text()="Mobile"]/following-sibling::td'))
            )
            item["dir_phone"] = element.text
        except:
            item["dir_phone"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][2]/table/tbody/tr/th[text()="Email"]/following-sibling::td'))
            )
            item["dir_email"] = element.text
        except:
            item["dir_email"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][3]/table/tbody/tr/th[text()="Office '
                     'Address"]/following-sibling::td/div'))
            )
            item["office_address"] = element.text
        except:
            item["office_address"] = "not found"
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][3]/table/tbody/tr/th[text()="Factory '
                     'Address"]/following-sibling::td/div'))
            )
            item["factory_address"] = element.text
        except:
            item["factory_address"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][4]/table/tbody/tr/th[text()="Employees"]/following-sibling::td'))
            )
            item["employee_number"] = element.text
        except:
            item["employee_number"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][4]/table/tbody/tr/th[text()="Production '
                     'Capacity"]/following-sibling::td'))
            )
            item["production_capacity"] = element.text
        except:
            item["production_capacity"] = "not found"

        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="company_info_card"][4]/table/tbody/tr/th[text()="Total '
                     'Machines"]/following-sibling::td'))
            )
            item["total_machines"] = element.text
        except:
            item["total_machines"] = "not found"
        item['source_URL'] = link
        item['source_name'] = 'BKMEA.COM'
        self.item.append(item)

    def save_to_json(self):
        make_dir(f"{self.info_path}")
        with open(f"{self.info_path}/data.json", 'w') as file:
            json.dump(self.item, file, indent=4)
