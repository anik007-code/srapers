import json
import time
import mysql.connector as mysql
from sqlalchemy import create_engine
from datetime import date
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.config_data import WAIT, MINI_WAIT, FILE, INFO_PATH, DATA_PATH, LINKS, ROOT_PATH, \
    IMAGE_PATH, LINK_PATH
from configs.config_db import DATABASE_NAME, PASSWORD, HOST_NAME, TABLE_NAME, USER_NAME
from functions import make_dir


class Wikipedia:
    def __init__(self, driver):
        self.wait = WAIT
        self.miniwait = MINI_WAIT
        self.site_link = LINKS
        self.driver = driver
        self.file = FILE
        self.img_path = f"{ROOT_PATH}/{DATA_PATH}/{IMAGE_PATH}"
        self.info_path = f"{ROOT_PATH}/{DATA_PATH}/{INFO_PATH}"
        self.link_path = f"{ROOT_PATH}/{DATA_PATH}/{LINK_PATH}"
        self.time = str(date.today())
        self.item = []
        self.company = []
        self.before_last_scrap = 0
        self.PREV_DAYS_SCRAPING = 1
        self.jobs = []
        self.category = []
        self.data_list = []
        # database
        self.db_name = DATABASE_NAME
        self.user_name = USER_NAME
        self.password = PASSWORD
        self.host_name = HOST_NAME
        self.table_name = TABLE_NAME
        self.column_names = []
        self.df = pd.DataFrame()
        # database
        self.run_scraper()

    def run_scraper(self):
        self.open_web_page()
        self.get_company_link()

    def open_link_new_tab(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

    def close_new_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def open_web_page(self):
        self.driver.get(self.site_link)

    def get_company_link(self):
        try:
            elements = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//table[@class="wikitable sortable jquery-tablesorter"]/tbody/tr/td[1]/a'))
            )
            for element in elements:
                link = element.get_attribute('href')
                # print(link)
                self.company.append(link)
            for item in self.company:
                self.open_link_new_tab(item)
                self.extract_data(item)
                self.close_new_tab()
        except Exception as e:
            print(f" error on company_link {e}")

    def extract_data(self, link):
        item = {}
        try:
            element = WebDriverWait(self.driver, self.miniwait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//th[text()="Website"]/following-sibling::td/span/a'))
            )
            item["website"] = element.get_attribute('href')
        except:
            item["website"] = "not found"
        item["source_name"] = "wikipedia"
        item["URL"] = link
        self.item.append(item)
        print(item)
    def connect_db(self):
        try:
            self.mydb = mysql.connect(db=self.db_name, user=self.user_name,
                                      password=self.password, host=self.host_name)
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {self.table_name} (top_company_vacancy_job_bd LONGTEXT);""")
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