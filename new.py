# -*- coding: utf-8 -*-
import re
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv
# from utils import remove_duplicates_links, chunkIt
from collections import defaultdict
import pymysql.cursors
import argparse
import os
import threading

print('Start at --- ' + str(datetime.now()))
source = '  TRIANGLE'

parser = argparse.ArgumentParser(description='pass in update argument')
parser.add_argument("--u", default=1, type=str, help="This is the 'update' variable true/false")
args = parser.parse_args()
update = args.u

now = datetime.now()

links_file = ' _triangle_properties_urls.csv'
if os.path.exists(links_file):
    pass
else:
    with open(links_file, 'w', newline='', encoding='utf-8') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['url'])


def get_links(main_url):
    print(update)
    if type(update) != int and update.lower() == 'false':
        print('REGULAR RUN')
        pass
    else:
        print('UPDATE')
        try:
            os.remove(links_file)
            os.remove(links_file.replace('.csv', '_ND.csv'))
            with open(links_file, 'w', newline='', encoding='utf-8') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow(['url'])
        except:
            pass
        with open(links_file, 'w', newline='', encoding='utf-8') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(['url'])
        # connection = pymysql.connect(host='datacollector.info',
        #                              port=3306,
        #                              user='datacoll_igor',
        #                              password='IgorPavlovic',
        #                              db='datacoll_realestate',
        #                              charset='utf8mb4',
        #                              cursorclass=pymysql.cursors.DictCursor)
        # cursor = connection.cursor()
        # delete_statement = '''DELETE FROM datacoll_realestate.PROPERTIES where source="''' + source + '''"'''
        # print('Delete', delete_statement)
        # cursor.execute(delete_statement)
        # print('DELETED!')
        # connection.commit()

    print(main_url)
    i = 1
    while 1:
        page_url = main_url.replace('properties-for-sale/', 'properties-for-sale/page/' + str(i) + '/')
        print(page_url)

        resp = requests.get(page_url)

        soup = BeautifulSoup(resp.content, 'html.parser')

        try:
            urls = soup.select('.thumbnail a')
        except:
            urls = []

        if len(urls) == 0:
            break
        else:
            for link in urls:
                print(link.attrs['href'])
                with open(links_file, 'a', newline='', encoding='utf-8') as myfile:
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                    wr.writerow([link.attrs['href']])
        i += 1
    # remove_duplicates_links(links_file)


def parse_props(threadName, start, end):
    # connection = pymysql.connect(host='datacollector.info',
    #                              port=3306,
    #                              user='datacoll_igor',
    #                              password='IgorPavlovic',
    #                              db='datacoll_realestate',
    #                              charset='utf8mb4',
    #                              cursorclass=pymysql.cursors.DictCursor)
    # cursor = connection.cursor()

    columns = defaultdict(list)
    with open(links_file.replace('.csv', '_ND.csv')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k, v) in row.items():
                columns[k].append(v)
    urls = columns["url"]

    for url in urls[start:end]:
        print(url)
        resp = requests.get(url)
        # with open('ppp.html', 'wb') as f:
        #     f.write(resp.content)
        soup = BeautifulSoup(resp.content, 'html.parser')
        url = url

        try:
            name = soup.select_one('.property_title.entry-title').get_text()
        except:
            name = ''

        try:
            address = soup.select_one('.location').get_text().replace('\n', ' ').strip()
        except:
            address = ''
        try:
            if 'villa' in name.lower():
                property_type = 'Villa'
            elif 'cottage' in name.lower():
                property_type = 'Cottage'
            elif 'apartment' in name.lower():
                property_type = 'Apartment'
            elif 'townhouse' in name.lower():
                property_type = 'Townhouse'
            elif 'plot' in name.lower():
                property_type = 'Plot'
            elif 'project' in name.lower():
                property_type = 'Project'
            elif 'building' in name.lower():
                property_type = 'Building'
            else:
                property_type = 'Other'
        except:
            property_type = ''

        try:
            coords = re.search('LatLng.(.*)', str(resp.content)).group(1)
        except:
            coords = ''

        try:
            latitude = re.search('([^,]*), ([^)]*)', coords).group(1)
        except:
            latitude = ''

        try:
            longitude = re.search('([^,]*), ([^)]*)', coords).group(2)
        except:
            longitude = ''

        try:
            updated_date_string = now.strftime('%Y-%m-%d %H:%M:%S')
        except:
            updated_date_string = ''

        try:
            price = float(soup.select_one('.pricebox  span:nth-child(1)').get_text().replace('.', '').replace('€', '').strip())
        except:
            price = None

        try:
            specific_features = []
            other_details_values = soup.select('.col2 li')
            for v in other_details_values:
                detail = v.get_text().replace('  \\xa0', '').strip()
                specific_features.append(detail)
        except:
            specific_features = []

        contact = '+351 911 857 585'

        try:
            ref = soup.select_one('.ref').get_text().replace('Ref: ', '')
        except:
            ref = ''

        professional = '  Triangle Properties'

        try:
            property_price = soup.select_one('.pricebox span:nth-child(1)').get_text().strip()
        except:
            property_price = ''

        try:
            area = int(
                re.search('(\d+)', soup.select_one('.buildarea span:nth-child(1)').get_text()).group(1).replace('Sq M',
                                                                                                                '').replace(
                    ' ', ''))
            price_all = int(price.replace(' ', '').replace('.', ''))
            div_ = price_all / area
            a = ("%.2f" % div_)
            price_per_square_meter = str(a)
        except:
            price_per_square_meter = ''

        try:
            descriptions_en = ''
            descriptions_en_all = soup.select('.description')
            for d in descriptions_en_all:
                descriptions_en += d.get_text().strip() + ' '
                print(d.get_text().strip())
            descriptions_en = descriptions_en.strip().replace('\n', ' ')
        except:
            descriptions_en = ''

        descriptions_pt = ''

        try:
            other_details = []
            other_details_ = soup.select('.propymetalist li span:nth-child(1)')
            other_details_labels = soup.select('.propymetalist li span:nth-child(2)')
            for v, l in zip(other_details_, other_details_labels):
                detail = l.get_text().replace('  \\xa0', '').strip() + ': ' + v.get_text().replace('  \\xa0',
                                                                                                   '').strip()
                other_details.append(detail)
        except:
            other_details = []

        equipment = []

        images = []
        try:
            images_list = soup.select('#slider li img')
            for im in images_list:
                images.append(im.attrs['src'].replace('-400x300', ''))
        except:
            images = []

        source = '  TRIANGLE'

        print(threadName, 'URL                                   ------ -------- ', url)
        print('name                           ---------------------- ', name)
        print('Address                           ------------------- ', address)
        # print('property_type                 ----------------------- ', property_type)
        # print('Lat                           ----------------------- ', latitude)
        # print('Long                           ---------------------- ', longitude)
        # print('updated_date_string          ------------------------ ', updated_date_string)
        print('Price                           --------------------- ', price)
        # print('Other details                           ------------- ', other_details)
        # print('Contact                           ------------------- ', contact)
        # print('Ref                           ----------------------- ', ref)
        # print('Professional                           -------------- ', professional)
        # print('property_price                           ------------ ', property_price)
        # print('price_per_square_meter                     ---------- ', price_per_square_meter)
        # print('descriptions pt                ---------------------- ', descriptions_pt)
        # print('descriptions en                ---------------------- ', descriptions_en)
        # print('specific_features            ------------------------ ', specific_features)
        # print('equipment                           ----------------- ', equipment)
        # print('images                           -------------------- ', images)
        print('\n')

        # insert_statement = '''
        #     INSERT IGNORE INTO datacoll_realestate.PROPERTIES
        #     (url, name, property_type, address, latitude, longitude, updated_date_string,
        #     price, other_details, contact, ref, professional, property_price, price_per_square_meter,
        #     descriptions_en, descriptions_pt, specific_features, equipment, images, source)
        #     VALUES
        #     (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        # val = (url, name, property_type, address, latitude, longitude, updated_date_string, price, str(other_details),
        #        contact, ref, professional, property_price, price_per_square_meter, descriptions_en, descriptions_pt,
        #        str(specific_features),
        #        str(equipment), str(images), source)
        # cursor.execute(insert_statement, val)
        # print('inserted')

        # connection.commit()

main_url = 'https://triangleproperties.pt/algarve-properties-exclusive-selection-of-luxury-properties-for-sale/?location&property_type&price_range&minimum_bedrooms&address_keyword&department=residential-sales'

get_links(main_url)

print('Done!')
print('Parsing properties....')

columns = defaultdict(list)
with open(links_file.replace('.csv', '_ND.csv')) as f:
    reader = csv.DictReader(f)
    for row in reader:
        for (k, v) in row.items():
            columns[k].append(v)
urls = columns["url"]
len_urls = len(urls)
print(len_urls)
# parts = chunkIt(range(len_urls), 5)
# print(parts)

for i in range(0, len(parts)):
    try:
        print(("Thread-"+str(i), parts[i], parts[i+1],))
        x = threading.Thread(target=parse_props, args=("Thread-"+str(i), int(parts[i]), int(parts[i+1]), ))
        x.start()
    except:
        continue

print('END at --- ' + str(datetime.now()))

