import json
import os
import mysql.connector as mysql
import pandas as pd
from sqlalchemy import create_engine
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.config_data import WAIT, MINI_WAIT, SITE_LINK, FILE, FILE_PATH, INFO_PATH, DATA_PATH, ROOT_PATH, LINK_PATH
from configs.config_db import DATABASE_NAME, PASSWORD, TABLE_NAME, USER_NAME, HOST_NAME
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
        # database
        self.db_name = DATABASE_NAME
        self.user_name = USER_NAME
        self.password = PASSWORD
        self.host_name = HOST_NAME
        self.table_name = TABLE_NAME
        self.column_names = []
        self.df = pd.DataFrame()
        self.run_scraper()

    def run_scraper(self):
        self.open_web_page()
        # self.click_on_add()
        # self.get_university_list()
        # self.get_university_link_list()
        self.extract_all_info()
        self.save_data()
        self.connect_db()
        self.get_db_columns()
        self.save_to_db()

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
            for element in elements:
                link = element.get_attribute('href')
                print(link)
                self.product.append(link)
            make_dir(f"{self.link_path}")
            with open(f"{self.link_path}/links.json", 'w') as file:
                json.dump(self.product, file, indent=4)
        except Exception as e:
            print(f"Error on 'get_category_list()' - {e}")

    def extract_all_info(self):
        try:
            file = f"{self.link_path}/links.json"
            if os.path.isfile(file):
                with open(file, 'r') as f:
                    data = json.loads(f.read())
            for book in data:
                # print(book)
                self.open_link_new_tab(book)
                self.extract_data(book)
                self.close_new_tab()
        except Exception as e:
            print(f"error on extract all info - {e}")

    def extract_data(self, link):
        item = {}
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[@class="tab-pane fade show active"]'))
            )
            item["overview_data"] = element.text
        except:
            item["overview_data"] = "not found"
        item["source_name"] = "DAAD.DE"
        item["URL"] = link
        self.item.append(item)
        print(item)

    def save_data(self):
        make_dir(f"{self.info_path}")
        with open(f"{self.info_path}/{self.file}", 'w') as file:
            json.dump(self.item, file, indent=4)

    def connect_db(self):
        try:
            self.mydb = mysql.connect(db=self.db_name, user=self.user_name,
                                      password=self.password, host=self.host_name)
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {self.table_name} (daad_data LONGTEXT);""")
            self.engine = create_engine(
                f"mysql+pymysql://{self.user_name}:{self.password}@{self.host_name}/{self.db_name}")
            print("connected to database")
        except Exception as e:
            print(f" error in connect_db() - {e}")

    def get_db_columns(self):
        self.df = pd.DataFrame(self.item)
        self.df.drop_duplicates()
        print(self.df)
        self.column_names = list(self.df.columns)
        self.column_names = sorted(self.column_names)
        print(self.column_names)
        for column in self.column_names:
            sql_statement = f"""alter table {self.table_name}
                                    add column {column} LONGTEXT;"""
            try:
                self.mycursor.execute(sql_statement)
            except Exception as e:
                print(e)

    def save_to_db(self):
        self.df.to_sql(self.table_name, con=self.engine, index=False, schema=self.db_name, if_exists='append',
                       chunksize=500)
