import time
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options

from configs.config_data import ROOT_PATH, DATA_PATH, DRIVER_PATH
from functions import make_dir
from post_ch_class.post_ch_class import PostScraper

driver_path = f"{ROOT_PATH}/{DATA_PATH}/{DRIVER_PATH}"
make_dir(f"{ROOT_PATH}/{DATA_PATH}")
make_dir(driver_path)

options = Options()
options.headless = False

chromedriver_autoinstaller.install(path=driver_path)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

scraper = PostScraper(driver)
