from selenium import webdriver
import chromedriver_autoinstaller
from configs.config_data import ROOT_PATH, DATA_PATH, DRIVER_PATH, WAIT
from functions import make_dir
from scraper_class.scraper_class import Skip

driver_path = f"{ROOT_PATH}/{DATA_PATH}/{DRIVER_PATH}"
make_dir(f"{ROOT_PATH}/{DATA_PATH}")
make_dir(driver_path)

chromedriver_autoinstaller.install(path=driver_path)
driver = webdriver.Chrome()
driver.maximize_window()

bkmea_scraper = Skip(driver)