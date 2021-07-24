import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = 'https://www.currys.co.uk/gbuk/rtx-3060-ti/components-upgrades/graphics-cards/324_3091_30343_xx_ba00013562-bv00313952/xx-criteria.html'

headers =  {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36' }

def check_for_gpus():
  page = requests.get(URL, headers=headers)

  soup = BeautifulSoup(page.content, "html.parser")

  currys_vendor_containers = soup.find_all("div", {"class": "ProductListItem__DivWrapper-pb4x98-8 bQkHoo"})

  for container in currys_vendor_containers:
    email_body = ""
    gpu_brand = container.find("span", {"data-product": "brand"}).get_text()
    title = container.find("span", {"data-product": "name"}).get_text()
    price = container.find("span", {"class": "ProductPriceBlock__Price-eXasuq hWYnYZ"}).get_text()
    link = container.find("a", {"class", "clickableArea"}).attrs['href']

    if (soup.find("li", {"class": "available"})):
      email_body = 'Title: {} {}, Price: {}\n\n Link: {}'.format(gpu_brand.upper(), title, price, link)
      send_email(email_body)

def send_email(contents):
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.ehlo()

  server.login('test@gmail.com', "test123")

  subject = 'Graphics Card in Stock'
  body = contents

  msg = '{}\n\n{}'.format(subject, body)

  server.sendmail(
    'opholroyd@gmail.com',
    'opphdev@gmail.com',
    msg
  )

  print("Email sent.")

while(True):
  check_for_gpus()
  time.sleep(60 * 60)