from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from configs.config_data import ROOT_PATH, DATA_PATH, DRIVER_PATH, INFO_PATH
from functions import make_dir
from tech_board_scraper_class.tech_board_scraper_class import TechnicalInstituteScraper

driver_path = f"{ROOT_PATH}/{DATA_PATH}/{DRIVER_PATH}"

make_dir(f"{ROOT_PATH}/{DATA_PATH}")
make_dir(driver_path)

# options = Options()
# options.headless = True

chromedriver_autoinstaller.install(path=driver_path)
driver = webdriver.Chrome()
driver.maximize_window()

scraper = TechnicalInstituteScraper(driver, info_path='DATA')
