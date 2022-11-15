# -*- coding: utf-8 -*-
import requests
import sys
import threading
from threading import Thread
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
success=0
inFileName = "XXX.txt" #目標IP.txt 格式:http://XXX/ or https://xxx/
sem = threading.Semaphore(100) #執行緒數量
bar_len = 60 #進度條長度

def url200(url,origin_url): #POC執行本體
    global success    
    try:            
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
        }
        r = requests.get(url=url, headers=headers, verify=False, timeout=5)
        if r.status_code == 200 :  #條件式
            success += 1  #條件成立成功數+1          
            body = """<br>            
            <a href="%s" target="_blank">%s </a>
            """%(url,origin_url)  #html寫入
            doc.write(body) 
        
    except Exception as error:
        pass
    finally:
        sem.release() #解鎖這個線程，開始其他線程。
    
    
def run():
    num=1   
    f = open(inFileName) 
    urls_data = f.readlines() #讀取txt內容
    total = str(len(urls_data)) #進度條總數
    for urls in urls_data:
        sem.acquire()
        if urls.find('http'):
            url = "http://" + urls.strip("\n") + "XXX" #POC網址
            origin_url = "http://" + urls.strip("\n") #原url
        else:
            url = urls.strip("\n") + "XXX" #POC網址
            origin_url = urls.strip("\n") #原url
        t1 = Thread(target=url200,args=(url,origin_url)) 
        t1.start()
        
        filled_len = int(round(bar_len * (num+1) / float(total))) # 以下為進度條
        percents = round(100.0 * (num+1) / float(total), 1)
        bar = ['='] * filled_len + ['-'] * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s %s/%s success:%s\r' % (''.join(bar), percents, '%', num, total, success))
        sys.stdout.flush()
        num = num + 1
    t1.join()

    html2 = """
    </div>
    </body>
    </html>"""
    doc.write(html2)
    doc.close()

doc = open("result.html", "a+" ,encoding="UTF-8") #開啟HTML寫入
html1 = """
    <html>
    <head></head>
    <style>
    body {
        background-color: #2b2b2b;
        color: #ccc;
    }
    a {
        background-color: transparent;
        text-decoration: none;
        outline: 0;
    }
    a:link {
        color:#FF0000;
        text-decoration:underline;
    }
    a:visited {
        color:#00FF00;
        text-decoration:none;
    }
    a:hover {
        color:#000000;
        text-decoration:none;
    }
    a:active {
        color:#FFFFFF;
        text-decoration:none;
    }
    </style>
    <body>
    <div>"""
doc.write(html1)

run()
# outFile.close()
