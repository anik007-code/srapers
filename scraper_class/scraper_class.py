import json
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.config_data import WAIT, MINI_WAIT, ROOT_PATH, DATA_PATH, INFO_PATH, \
    LINK_PATH, FILE, LINKS, IMAGE_PATH
from functions import make_dir


class Scraperclass:
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
        self.category = []
        self.data_list = []
        self.run_scraper()

    def run_scraper(self):
        self.open_web_page(self.site_link)
        self.get_category()
        self.get_company()

    def open_web_page(self, link):
        self.driver.get(link)

    def open_link_new_tab(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

    def close_new_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def get_category(self):
        try:
            elements = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//div[@class="col-md-auto font-weight-medium text-center text-md-start"]/a')))
            for element in elements:
                link = element.get_attribute('href')
                print(link)
                self.category.append(link)
        except Exception as e:
            print(f" error on get_company -{e}")

    def get_company(self):
        try:
            for category in self.category:
                self.open_link_new_tab(category)
                flag = True
                while flag:
                    try:
                        flag = True
                        self.get_company_list()
                        element = WebDriverWait(self.driver, self.wait).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                 '//a[text()="Next"]'))
                        )
                        self.driver.execute_script("arguments[0].click();", element)
                    except:
                        flag = False
                        print(f"{flag}")
                self.close_new_tab()
        except Exception as e:
            print(f"Error on get company{e}")

    def get_company_list(self):
        try:
            elements = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//a[@class="job-title job-link"]'))
            )
            for element in elements:
                link = element.get_attribute('href')
                self.company.append(link)
                print(link)
            make_dir(f"{self.link_path}")
            with open(f"{self.link_path}/company_link.json", 'w') as file:
                json.dump(self.company, file, indent=4)
        except Exception as e:
            print(f" error on {e}")
