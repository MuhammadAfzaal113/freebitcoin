
base_uri = 'https://freebitcoin.io/'

static_base = 'https://freebitcoin.io/'

import os
import re
import requests
from bs4 import BeautifulSoup as soup


def download_images(url):
    g = requests.get(url)

    parsed = soup(g.content, 'lxml')

    images = parsed.find_all('img')

    for img in images:
        img_link = img.get('src')

        filtered_img_link = img_link.split('?')[0]

        file_name = filtered_img_link.lstrip('img/')

        # Try to get the image byte
        full_image_url = static_base + img_link

        # Get the dir name
        dir_name = os.path.dirname(file_name)

        # check if this is a valid link
        if dir_name.find(':') != -1:
            continue
            
        # Create directory
        try:
            if dir_name:
                os.makedirs(dir_name)
        except FileExistsError as e:
            pass
        
        # Check if file is not already there
        if not os.path.exists(file_name):
            response = requests.get(full_image_url)

            if response.status_code == 200:
                print(full_image_url)
                with open(file_name, 'wb') as file:
                    file.write(response.content)



def download_assets():
    download_images(base_uri)

# save_pages()
download_assets()