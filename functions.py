import logging
import os
import shutil
import requests


def make_dir(dir_name):
    try:
        os.mkdir(dir_name)
        print("Directory ", dir_name, " created.")
    except FileExistsError:
        print("Directory ", dir_name, " already exist.")


def image_downloader(img_url, img_name, img_path):
    try:
        make_dir(img_path)
        res = requests.get(img_url, stream=True)
        image_file_name = f"{img_path}/{img_name}.jpg"
        # urllib.request.urlretrieve(img_url, image_file_name)
        if res.status_code == 200:
            with open(image_file_name, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ', image_file_name)
        else:
            print('Image Couldn\'t be retrieved')
    except Exception as e:
        logging.exception(e)
