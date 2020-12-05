from selenium import webdriver
import time

# 用户url
url = 'https://www.toutiao.com/i6884936118685729293/?tt_from=copy_link&utm_campaign=client_share&timestamp=1604805670&app=news_article&utm_source=copy_link&utm_medium=toutiao_android&use_new_style=1&req_id=2020110811210901002605921626BFBE51&group_id=6884936118685729293'
# google驱动的下载，下载win32版
executable_path="C:\\Users\\30270\\Downloads\\Compressed\\chromedriver_win32\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=executable_path)
# 开始请求
driver.get(url=url)
time.sleep(5)
# 让滚动条向下滚动到底部，多滚动几次，根据情况而定
js = "var q=document.documentElement.scrollTop=200"
driver.execute_script(js)
time.sleep(2)
js = "var q=document.documentElement.scrollTop=200"
driver.execute_script(js)
time.sleep(2)
js = "var q=document.documentElement.scrollTop=200"
driver.execute_script(js)
time.sleep(2)
js = "var q=document.documentElement.scrollTop=200"
driver.execute_script(js)
time.sleep(2)
js = "var q=document.documentElement.scrollTop=200"
driver.execute_script(js)
# 找到所有网址
weblist=driver.find_elements_by_xpath("""//*[@class = 'link title']""")
i=0
li=[]
for web in weblist:
    url=web.get_attribute("href")
    print(url)
    li.append(url)
# 无限循环浏览
while True:
    for u in li:
        driver.get(u)
        time.sleep(1)
        js = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)
        print(i)
        i+=1
        time.sleep(1)

driver.quit()