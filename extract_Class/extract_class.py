import json
import time
import pandas as pd
import requests
from configs.config_data import INFO_PATH, DATA_PATH, FILE, FILE_PATH, API_URL, ROOT_PATH
from functions import make_dir


class TestScraper:
    def __init__(self, driver):
        self.driver = driver
        self.info_path = f"{ROOT_PATH}/{DATA_PATH}/{INFO_PATH}"
        self.data_path = DATA_PATH
        self.file = FILE
        self.url = API_URL
        self.data = FILE_PATH
        self.item = []
        self.data_list = []
        self.page = int()
        self.run_scraper()

    def run_scraper(self):
        self.extract_data()

    def extract_data(self):
        for x in range(0, 33538):
            req = requests.get(f"{self.url}{x}")
            req = pd.DataFrame(req.json())
            hit = req['hits']
            main_dict = hit['hits']
            for key in main_dict:
                for i, j in key.items():
                    if i == "_source":
                        sub_dict = key[i]
                        print(sub_dict)
                        self.item.append(sub_dict)
                make_dir(f"{self.info_path}")
                with open(f"{self.info_path}/{self.file}", 'w') as file:
                    json.dump(self.item, file, indent=4)

