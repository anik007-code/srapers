import os

API_URL = "https://www.workingnomads.com/jobsapi/job/_search?sort=expired:asc,premium:desc,pub_date:desc&_source=company,category_name,description,locations,location_base,salary_range,salary_range_short,number_of_applicants,instructions,id,external_id,slug,title,pub_date,tags,source,apply_url,premium,expired,use_ats,position_type&size=1&from="
ROOT_PATH = os.getcwd()
DATA_PATH = "DATA"
DRIVER_PATH = "DRIVER"
INFO_PATH = "INFO"
FILE = "data.json"
FILE_PATH = "INFO"
