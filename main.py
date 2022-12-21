from bkmea_scraper_class.bkmea_Scraper_Class import BkmeaScraper
from selenium import webdriver
import chromedriver_autoinstaller
from configs.config_data import ROOT_PATH, DATA_PATH, DRIVER_PATH, WAIT
from functions import make_dir

driver_path = f"{ROOT_PATH}/{DATA_PATH}/{DRIVER_PATH}"
make_dir(f"{ROOT_PATH}/{DATA_PATH}")
make_dir(driver_path)

chromedriver_autoinstaller.install(path=driver_path)
driver = webdriver.Chrome()
driver.maximize_window()

bkmea_scraper = BkmeaScraper(driver)