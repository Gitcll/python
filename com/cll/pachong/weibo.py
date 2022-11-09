#拿到页面源代码  requests
#通过re来提取想要的有效信息  re模块

import requests
import re
from bs4 import BeautifulSoup

url = 'https://movie.douban.com/top250'
header = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
resp = requests.get(url, headers=header)
page_content = resp.text #爬取到的页面源代码
child_page = BeautifulSoup(page_content, "html.parser")
resp.close()
obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)</span>', re.S)
result = obj.finditer(page_content)
for i in result:
    print(i.group("name"))

child_page.select(".hd a span")
print()