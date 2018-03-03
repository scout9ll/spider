import requests
from bs4 import BeautifulSoup
import re
import os
import pymysql
import gevent
import gevent.monkey
import urllib
import json
import queue
import threading
import time
gevent.monkey.patch_all()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 ',
    "cookie": "_ga=GA1.2.771265069.1517499810; _gid=GA1.2.1031804230.1519482298"
}
def download(picture_url, picture_add):

    try:
        urllib.request.urlretrieve(picture_url, picture_add)
        print(picture_add,"下载完成")
    except:
        errorurls.append([picture_url,picture_add])



def createfile(target_tilte):
    global file_name

    #file_name="gakkipictures/"+dealed_link[-3]+dealed_link[-2]

    file_name="gakkipictures_携程+/"+target_tilte.replace(u'\u3000', u'').replace("/","").replace("\n","").replace("?","").replace("\t","")
    if not os.path.exists(file_name):


        os.makedirs(file_name)

        print("已创建："+file_name)


    else:

        print(file_name+"文件已存在")

def find_src(url,url_text):#找出所有的图片src
    try:
        data = requests.get(url, headers=headers)

        soup = BeautifulSoup(data.text, 'lxml')
        ss=soup.find("div",id=os.path.basename(url))
        target_tag = ss.find_all("a",href=re.compile("(.jpg|.png)"))


        wow=list(picture_tag.get("href") for picture_tag in target_tag)
        if wow ==[]:
            print("图片为空：",url)
        else:
            for picture_url in wow:
                print(picture_url,url_text)
                data = (url_text, picture_url)
                cursor.execute(sql % data)
                connect.commit()
                print('成功插入', cursor.rowcount, '条数据')


    except:
        print("url下载失败:",url)



def add_url(host_url):#找出所有拥有图片的子链接并下载url和title入数据库
    bigdata=requests.get("http://marsar.club/page-953/page-948/",headers=headers)
    soup1 = BeautifulSoup(bigdata.text,"lxml")
    url_tag=soup1.find_all(href=re.compile("http://marsar.club/[A-Za-z]+/post"))
    for url1 in url_tag:
        url=url1.get("href")[0:-1]
        url_text=url1.get_text()
        find_src(url,url_text)

#数据库链接操作
connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='87955626',
    db='t1',
    charset='utf8'
)

errorurls=[]

sql = "INSERT INTO gakki (name, url) VALUES ( '%s', '%s')"
cursor = connect.cursor()
cursor.execute("SELECT * FROM gakki")
rows = cursor.fetchall()

def read_url(row): # 下载数据库文件（title 和url）
        #row=q.get()
        createfile(row[1])

        picture_add=file_name+'/'+os.path.basename(row[2])
        picture_url=row[2]
        download(picture_url,picture_add)

if __name__=="__main__":
    start=time.time()
    for row in rows:
        #新开一个线程
        try:
            thread = threading.Thread(target=read_url,args=(row,))
            thread.start()
        except:
            print("创建新线程失败！")
    """
    q = queue.Queue()                               #可使用列队
    for row in rows:
        q.put(row)
    t1 = threading.Thread(target=read_url, args=(q,), name="thread1")
    t2 = threading.Thread(target=read_url, args=(q,), name="thread2")
    t3 = threading.Thread(target=read_url, args=(q,), name="thread3")
    t4 = threading.Thread(target=read_url, args=(q,), name="thread4")
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    """
    end=time.time()
    print("运行时间",end-start)
    """file_name1= 'errorurls.json'  
    with open(file_name1, 'r') as file_object:
        contents = json.load(file_object)
 """
    file_name1="errorurls.json"         # 将下载失败的数据为存入json格式
    with open(file_name1,"w") as file_object:
        json.dump(errorurls,file_object)
