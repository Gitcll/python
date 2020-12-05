import requests
import re
import user_agent#这个库是改变user-agent头的
import threading
import time
#print(user_agent.generate_user_agent())
url="https://blog.csdn.net/zhiboqingyun/article/details/109498623"#这里是你想要刷流浪数量的网址，如果需要替换即可
def res (ip):
    proxies = {
        "http": "http://" + ip[0] + ":" + ip[1],
        "https": "http://" + ip[0] + ":" + ip[1],
    }
    try:
        res = requests.get("http://www.baidu.com", proxies=proxies, timeout=3)
        res1 = requests.get(url, proxies=proxies, timeout=3)#这个网址是我写的一个博客地址
        print(ip, "能够使用")

    except Exception as e:
        pass
        #print(ip, "不能使用")
def getip(i):
        headers = {
            "User-Agent": ""+user_agent.generate_user_agent()+""
        }
        url="https://www.xicidaili.com/nn/{}".format(i)
        response=requests.get(url=url,headers=headers)
        #print(response.text)
        html=response.text
        ips=re.findall("<td>(\d+\.\d+\.\d+\.\d+)</td>",html,re.S)
        ports=re.findall("<td>(\d+)</td>",html,re.S)
        print(ips)
        print(ports)
        for ip in zip(ips,ports):
            threading.Thread(target=res, args=(ip,)).start()
            #print(ip)
for i in range(1,3000):
    getip(i)
    time.sleep(5)#如果过快的爬取代理网站会被禁ip，这里我已经被禁了很多次-_-