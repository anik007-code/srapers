import time
from datetime import date
import pandas as pd
from selenium.webdriver.common.by import By
from configs.config_data import SITE_LINK, WAIT, MINI_WAIT, ROOT_PATH, DATA_PATH, FILE_NAME, INFO_PATH, LINK_PATH


class Skip:
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
        category_links = []
        categories = self.driver.find_elements(By.XPATH, '//a[@class="ui builder_button purple"]')
        for category in categories:
            category = category.get_attribute('href')
            category_links.append(category)
        for category_link in category_links:
            self.open_link_new_tab(category_link)
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
                        # [cleaned_link.append(x) for x in page_dict if x not in cleaned_link]
                    for link in cleaned_link:
                        self.get_company_link_list()
                        self.open_link_new_tab(link)
                        self.close_new_tab()
                try:
                    pages = self.driver.find_elements(By.XPATH, '//a[@class="number"]')
                    page_dict = []
                    for page in pages:
                        page = page.get_attribute('href')
                        page_dict.append(page)
                    for page_links in page_dict:
                        self.get_company_link_list()
                        self.open_link_new_tab(page_links)
                        self.close_new_tab()
                    try:
                        self.get_company_link_list()
                    except:
                        flag = False
                        print(flag)
                except:
                    flag = False
                    print(flag)
            except:
                flag = False
                print(f"{flag}")
            self.close_new_tab()

    def get_company_link_list(self):
        try:
            elements = self.driver.find_elements(By.XPATH, '//h2[@class="post-title entry-title"]/a')
            for element in elements:
                element = element.get_attribute('href')
                print(element)
        except Exception as e:
            print(f" error on get_company-link() - {e}")
