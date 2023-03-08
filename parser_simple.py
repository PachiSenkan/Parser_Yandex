import requests
import re
from bs4 import BeautifulSoup as bs
import pandas as pd


def pars(URL_TEMPLATE, category_id, file_name):
    HEADERS ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0 (Edition Yx GX)',
        'x-lavka-web-city': '65'
    }

    r = requests.get(URL_TEMPLATE, headers=HEADERS)
    print(r.status_code)
    #print(r.text)

    soup = bs(r.text, "html.parser")
    product_names = soup.find_all('div', class_='cnopttn pyi2ep2 l1dy0xfh v1rqy0wm')
    print(len(product_names))
    file = open(file_name, "w", encoding="utf-8")
    for name in product_names:
      #print('https://lavka.yandex.ru' + name.a['href'])
       temp_url = 'https://lavka.yandex.ru' + name.a['href']
       r1 = requests.get(temp_url, headers=HEADERS)
       #print(r1.status_code)
       # print(r.text)
       soup1 = bs(r1.text, "html.parser")
       pr_image = soup1.find('img', class_='i1s3mcod i1shnzmq')
       pr_category = soup1.find_all('span', class_='t18stym3 bw441np r88klks r1dbrdpx t1dh4tmf l14lhr1r')
       pr_name = soup1.find('h1', class_='t5c3shz t18stym3 hbhlhv b1ba12f6 b1wwsurb n1wpn6v7 l14lhr1r')
       pr_price = soup1.find('span', class_='ta7w9v t18stym3 t38p0ru b1ba12f6 bkuxkry t1wnuyqt l14lhr1r')
       pr_mass = soup1.find('span', class_='s1l37y20 t18stym3 b1clo64h r88klks r1b0wfc3 lc0zwt5 l14lhr1r')
       pr_kbzu = soup1.find_all('dd', class_='t18stym3 b1clo64h m493tk9 m1fg51qz n1pe8tpi l14lhr1r')
       pr_nutr = pr_kbzu[0]
       pr_belk = pr_kbzu[1]
       pr_fats = pr_kbzu[2]
       if len(pr_kbzu) == 4:
            pr_carbs = pr_kbzu[3]
       url = 'https://lavka.yandex.ru' + name.a['href']
       print(url)
       #print(pr_image.attrs.get('src'))
       image = pr_image.attrs.get('src')
      # print(image)
       #print(pr_name.text)
       name = pr_name.text
       category = pr_category[2].text
      # print(name)
       #print(pr_price.text)
       price = pr_price.text
       ll = len(price)
       price = price[:ll-2]
       #print(price)
       #print(pr_mass.text)
       mass = pr_mass.text.partition('г')[0]
       l = len(mass)
       mass = mass[:l-1]
       #print(mass + 'aaa')
      # print(pr_nutr.text)
       nutr = pr_nutr.text
      # print(nutr)
      # print(pr_belk.text)
       prot = pr_belk.text
      #print(pr_fats.text)
       fats = pr_fats.text
      # print(fats)
       #print(pr_carbs.text)
       carbs = pr_carbs.text
      # print(carbs)
       insert_string = 'Insert into catalog (name; category; price; mass; nutrition; proteins; fats; carbs; url; image) values (' \
             + 'ABOBA' + name + 'ABOBA' + '; ' \
             + str(category_id) + '; ' \
             + price + '; ' \
             + mass + '; ' \
             + nutr + '; ' \
             + prot + '; ' \
             + fats + '; ' \
             + carbs + '; ' \
             + 'ABOBA' + url + 'ABOBA' + '; ' \
             + 'ABOBA' + image + 'ABOBA' + ')+'
       file.write(insert_string)
       file.write('\n')
       print(insert_string)
    file.close()

#Пример использования
links = ['https://lavka.yandex.ru/213/category/beef_pork?resetScroll=true',
         'https://lavka.yandex.ru/213/category/ryba_i_moreprodukty?resetScroll=true']
files = ['мясо_птица.txt',
         'рыба.txt']
id = 26
#pars('https://lavka.yandex.ru/65/category/cheese/syrnye_narezki', id, 'sir.txt')
for num in range(2):
    pars(links[num], id, files[num])
    id = id+1

