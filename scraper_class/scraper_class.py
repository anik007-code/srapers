import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configs.config_data import WAIT, MINI_WAIT, SITE_LINK, FILE, FILE_PATH, INFO_PATH, DATA_PATH, LINK_PATH, ROOT_PATH
from functions import make_dir


class Rokomari:
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
        # self.get_category_link()
        self.extract_all_info()

    def open_link_new_tab(self, link):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

    def close_new_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def open_web_page(self):
        self.driver.get(self.site_link)

    def get_product_link(self):
        flag = True
        while flag:
            try:
                add = WebDriverWait(self.driver, self.wait).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         '//div[@id="js--entry-popup"]/div/button/i'))
                )
                add.click()
            except:
                try:
                    # action = ActionChains(self.driver)
                    flag = True
                    self.get_product_list()
                    btn = WebDriverWait(self.driver, self.miniwait).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             '//a[text()="Next"]'))
                    )
                    self.driver.execute_script("arguments[0].click();", btn)
                    # action.move_to_element(btn).click().perform()
                    print(flag)
                except:
                    flag = False
                    print(flag)

    def get_category_link(self):
        category = []
        try:
            elements = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//ul[@class="list-inline list-unstyled categoryList"]/li/div/a'))
            )
            for element in elements:
                link = element.get_attribute('href')
                category.append(link)
            for links in category:
                self.open_link_new_tab(links)
                try:
                    self.get_product_link()
                    try:
                        add = []
                        add_all = WebDriverWait(self.driver, self.wait).until(
                            EC.presence_of_all_elements_located(
                                (By.XPATH,
                                 '//a[text()="View All"]'))
                        )
                        for elem in add_all:
                            elem = elem.get_attribute('href')
                            add.append(elem)
                        for add_link in add:
                            self.open_link_new_tab(add_link)
                            self.get_product_link()
                            self.close_new_tab()
                    except:
                        print("pagination not found")
                except:
                    print("No pagination")
                self.close_new_tab()
        except Exception as e:
            print(f"Error on 'get_category_list()' - {e}")

    def get_product_list(self):
        try:
            elements = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH,
                     '//div[@class="book-list-wrapper "]/a'))
            )
            for element in elements:
                element = element.get_attribute('href')
                print(element)
                self.product.append(element)
            # make_dir(f"{self.link_path}")
            with open(f"{self.link_path}/books_link.json", 'w') as file:
                json.dump(self.product, file, indent=4)
        except Exception as e:
            print(f" error on get_product_list - {e}")

    def extract_all_info(self):
        try:
            for book in self.product:
                self.open_link_new_tab(book)
                self.extract_data(book)
                self.close_new_tab()
        except Exception as e:
            print(f"error on extract all info - {e}")

    def extract_data(self, link):
        item = {}
        try:
            WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//a[text()=" Specification "]'))
            ).click()
        except:
            print("Specification not found")

        try:
            item['books_name'] = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//td[text()="Title"]/following-sibling::td'))
            ).text
        except:
            item['books_name'] = "not found"

        try:
            item['auther'] = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//td[text()="Author"]/following-sibling::td'))
            ).text
        except:
            item['auther'] = "not found"
        try:
            item['publisher'] = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//td[text()="Publisher"]/following-sibling::td'))
            ).text
        except:
            item['publisher'] = "not found"

        try:
            item['edition'] = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//td[text()="Edition"]/following-sibling::td'))
            ).text
        except:
            item['edition'] = "not found"

        try:
            item['total_page'] = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//td[text()="Number of Pages"]/following-sibling::td'))
            ).text
        except:
            item['total_page'] = "not found"

        try:
            item['country'] = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//td[text()="Country"]/following-sibling::td'))
            ).text
        except:
            item['country'] = "not found"

        try:
            item['language'] = WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//td[text()="Language"]/following-sibling::td'))
            ).text
        except:
            item['language'] = "not found"

        item['source_url'] = link
        item['source_name'] = "ROKOMARI"
        self.item.append(item)
        # make_dir(f"{self.info_path}")
        with open(f"{self.info_path}/data.json", 'w') as file:
            json.dump(self.item, file, indent=4)
