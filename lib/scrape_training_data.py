from bs4 import BeautifulSoup
import requests
import os
import shutil
import csv

URL = "https://tijdregistratie.jahoma.nl/photo/index?Photo_Page={}"
TOTAL_PAGES = 10
FILE_DOWNLOAD = './training_data'
DOWNLOAD=False
photo_csv = 'file_path,bib'

for i in range(0, TOTAL_PAGES):
    pic_url = URL.format(i)

    r = requests.get(pic_url)
    soup = BeautifulSoup(r.text)

    photo_divs = soup.findAll("div", {"class": "photo-container"})

    j=0
    for photo_div in photo_divs:
        race_number_text = photo_div.find('ul', {"class":"description"})        
        race_number_text = race_number_text.find('li',{'class':'name'}).text
        number = race_number_text.split("(")[1][:-1]

        print("Found picture of number ", number)
        print("Downloading picture")

        photo_holder = photo_div.find('div',{'class':'photo'}).find('img')

        img_src = 'https:'+photo_holder['src'].replace('_100.JPG', '_500.JPG')
        print(img_src)
        if DOWNLOAD:
            with open(os.path.join(FILE_DOWNLOAD, 'image{}_{}.jpg'.format(i, j)), 'wb') as ofile:
                img_file = requests.get(img_src, stream=True)
                img_file.raw.decode_content = True
                shutil.copyfileobj(img_file.raw, ofile)
                del img_file


        photo_csv+='\n{},{}'.format(os.path.join(FILE_DOWNLOAD, 'image{}_{}.jpg'.format(i, j)), number)
            

        j+=1

print(photo_csv)
with open(os.path.join(FILE_DOWNLOAD,'labels.csv'), 'wb') as ofile:
    writer = csv.writer(ofile)
    writer.writerows(photo_csv)