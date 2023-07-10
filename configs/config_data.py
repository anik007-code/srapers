import os

SITE_LINK = "https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=Data%20Science" \
            "&degree%5B%5D=1&degree%5B%5D=2&lang%5B%5D=1&lang%5B%5D=2&fos=&cert=&admReq=&langExamPC=&langExamLC" \
            "=&langExamSC=&langDeAvailable=&langEnAvailable=&lvlDe%5B%5D=&lvlEn%5B%5D=&modStd%5B%5D=&cit%5B%5D=&tyi" \
            "%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&dur=&subjects" \
            "%5B%5D=&limit=10&offset=&display=list"
ROOT_PATH = os.getcwd()
DATA_PATH = "DATA"
DRIVER_PATH = "DRIVER"
INFO_PATH = "INFO"
LINK_PATH = "LINK"
FILE = "data.json"
FILE_PATH = "INFO"
MINI_WAIT = 1
WAIT = 20
MEDIUM_WAIT = 120
LONG_WAIT = 240