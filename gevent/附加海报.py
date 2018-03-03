import requests
from bs4 import BeautifulSoup
import re
from  gakki import download,createfile,requesturl,createname
import gevent
import gevent.monkey
gevent.monkey.patch_all()
import datetime
s = requests.session()
s.keep_alive = False
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 ',
    "cookie": "_ga=GA1.2.771265069.1517499810; _gid=GA1.2.1031804230.1519482298"
}
all_targets=[]
all_urls=[]
def find_targeturl(host_url):
    data = requests.get(host_url,headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})
    soup = BeautifulSoup(data.text,"lxml")
    url_soup=soup.find_all(href=re.compile("http://marsar.club/[A-Za-z]+/post"))
    for target_tag in url_soup:

        target_url=target_tag.get("href")
        print(target_url)
        target_tilte=target_tag.get_text()
        all_urls.append(target_url)
        all_targets.append(target_tilte)
find_targeturl("http://marsar.club/page-953/page-948/")
n=0
all_picture_url=[]
for url in all_urls:
    try:
        for picture_url in requesturl(url,headers,r"http://ecx.images-amazon.com/images/.+?.jpg"):


            if picture_url not in all_picture_url:
                n = n + 1
                all_picture_url.append(picture_url)
                picture_add = "post" +"/%s.jpg "% n
            #download(picture_url,picture_add)
                print(picture_add)
                ge = [gevent.spawn(download, picture_url, picture_add)]

                print(picture_url)
            else:
                pass


    except:
        print("错误：",url)
gevent.joinall(ge)