import os
import csv
import requests
import pandas as pd
from PIL import Image
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

import scrape.settings as settings

def get_page(url):

    page_data = requests.get(url=url)
    page_data.text

    html_text = page_data.text
    page = bs(html_text, 'html.parser')

    return page

def get_data(page):

    label_urls = []
    
    imgs = page.find_all('img')
    imgs = [img for img in imgs if 'gallery-image' in img.attrs.get('class',  [])]

    for img in imgs:

        label_urls.append(
            (
            img.attrs.get('data-title', None),
            img.attrs.get('src', None),
            img.attrs.get('data-caption', None)
            )
        )

    return label_urls

def save_data(data, to=None, mode='a'):

    if not to:
        to = settings.SAVE_URL
    
    path = os.path.join(to, settings.SAVE_NAME)
    just_created = not os.path.exists(path)

    with open(path, mode) as csvf:
        csv_writer = csv.writer(csvf)

        if just_created:
            csv_writer.writerow(['title','url','caption'])
        
        for row in data:
            csv_writer.writerow(list(row))
        

def iter_pages(*functions):

    f_list = list(functions)
    
    page_from = settings.PAGE_FROM
    page_to = settings.PAGE_TO

    for i in tqdm(range(page_from, page_to)):
        print(f'On page {i}')

        path = settings.PAGE_URL + str(i)

        y = path
        for f in f_list:
            y = f(y)
    
    print('should be done, check csv file!')


def download(csvf, ignore=True):
    
    df = pd.read_csv(csvf)

    if ignore:
        with open(settings.IGNORE_FILE, 'r') as f:
            ignore_set = set( x.strip().replace('\\', '') for x in f.readlines())
            

    for index, row in tqdm(df.iterrows()):

        if row['title'].strip() in ignore_set:
            continue
        
        r = requests.get(row['url'], stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True

            im = Image.open(r.raw)

            caption = "".join(row['caption'].strip().split())
            title = "".join(row['title'].strip().split())
            
            save_path = os.path.join(settings.SAVE_DB, f'{index}_{caption}_{title}.png')
            im.save(save_path, format='png')
        
    del df