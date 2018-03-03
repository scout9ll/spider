import requests
import urllib
from bs4 import BeautifulSoup
import time
import os
import re
import asyncio

def createfile(target_tilte):
    global file_name

    #file_name="gakkipictures/"+dealed_link[-3]+dealed_link[-2]

    file_name="gakkipictures_携程/"+target_tilte.replace(u'\u3000', u'').replace("/","").replace("\n","")

    if not os.path.exists(file_name):

        os.makedirs(file_name)

        print("已创建："+file_name)


    else:

        print(file_name+"文件已存在")



def createname(picture_url):

    dealed_link=picture_url.split("/")

    picture_name=dealed_link[-1]

    return picture_name


def requesturl(url,headers,x):


    try:
        data = requests.get(url, headers=headers,)

        soup = BeautifulSoup(data.text, 'lxml')


        target_tag= soup.find_all(src=re.compile(x))


        return list(picture_tag.get("src") for picture_tag in  target_tag)
    except:
        pass
def download(picture_url, picture_add):

    try:
        urllib.request.urlretrieve(picture_url, picture_add)
        print(picture_add,"下载完成")
    except:
        print("error:", picture_url)















"""
all_urls=[]
tasks=[]

def find_targeturl(host_url):
    data = requests.get(host_url,headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})
    soup = BeautifulSoup(data.text,"lxml")
    url_soup=soup.find_all(href=re.compile("http://marsar.club/news/post"))
    u=62
    for target_tag in url_soup:

        target_url=target_tag.get("href")
        target_tilte=target_tag.get_text()
        try:
            createfile(target_tilte)
        except:
            pass
        all_urls.append(target_url)
find_targeturl("http://marsar.club/page-953/page-948/")
for target_url in all_urls:
    print(target_url)
    tasks.append(download(r"http://marsar.club/wp-content/uploads/\d{4}\/\d{2}\/photo[A-Za-z0-9]+\.jpg*",target_url))
loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(asyncio.gather(*tasks[0:2]))
loop.close()
"""

