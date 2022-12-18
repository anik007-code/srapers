from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options

from baira_scraper_class.baira_scraper_class import BairaScraper
from configs.config_data import ROOT_PATH, DATA_PATH, DRIVER_PATH, INFO_PATH
from functions import make_dir

driver_path = f"{ROOT_PATH}/{DATA_PATH}/{DRIVER_PATH}"

make_dir(f"{ROOT_PATH}/{DATA_PATH}")
make_dir(driver_path)

options = Options()
options.headless = True
chromedriver_autoinstaller.install(path=driver_path)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

star = BairaScraper(driver)