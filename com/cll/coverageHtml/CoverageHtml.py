from com.cll.io.FileIO import *
from com.cll.io.commFile import *
from bs4 import BeautifulSoup
import re
import pandas as pd

path = "C:\\Users\\30270\\HBuilderProjects"
#查找当前文件下的第一层级文件夹
fileDirectoryArr = get_directory(path)
#e = 0代表生成excel顺序
e = 0
for fileDirectory in fileDirectoryArr:
    #初始化
    fileNameArr.clear()
    #遍历当前文件下的第一层级文件夹下所有的html
    fileNameArr = get_fileName(fileDirectory, ".html")
    #w = 0代表生成sheet顺序
    w = 0
    #创建以第一层级文件夹Excel文件
    writer = pd.ExcelWriter("excel 样例" + str(e) + ".xlsx", mode='w', engine='openpyxl')
    e += 1
    for file in fileNameArr:
        if str(file).endswith("index.html"):
            print(file)
            #读取index.html文件,以数组的形式返回
            date = read_file_getArrayData(file)
            #解析当前index.html
            child_page = BeautifulSoup(str(date), "html.parser")
            #查找当前index中tbody标签
            tbody = child_page.find("tbody")
            if tbody != None:
                #初始化字典
                dateArr11 = {}
                #设置sheet默认标题行
                dateArr11["biaotou"] = ['プロジェクト名', 'Javaファイル', 'カバー率']
                #i = 0标记dateArr11中key不能重复
                i = 0
                #tbody.select('tr')查找tbody下所有的tr标签
                for tbodyChildren in tbody.select('tr'):
                    #使用正则匹配当前tr标签中存在百分比
                    pattern = re.compile(r'(?<=>)(\d+%)(?=<)')
                    res = pattern.search(str(tbodyChildren))
                    if res != None:
                        #初始化,存放数据
                        dateArr = []
                        #获取项目名<td id="a0"><a href="App.html" class="el_class">App</a></td>
                        dateArr.append(child_page.select('#breadcrumb a.el_bundle')[0].string)
                        #child_page.title.string获取包名
                        #tbodyChildren.td.a.string获取class名
                        dateArr.append(child_page.title.string + '.' + tbodyChildren.td.a.string)
                        #获取覆盖率百分比
                        dateArr.append(res.group())
                        #将数据存放入字典
                        dateArr11[child_page.title.string + '.' + tbodyChildren.td.a.string + str(i)] = dateArr
                        i += 1
                #dateArr11数据格式, 如: {"col1": [1, 2, 3], "col2": [4, 5, 6], "col3": [7, 8, 9]}
                #默认输出为竖向排列
                #T代表可以将数据横向排列,输出表格中
                data = pd.DataFrame(dateArr11).T
                #写入数据
                data.to_excel(writer, sheet_name="这是第" + str(w) + "个sheet",index=False)
                w += 1
    #保存excel,并关闭
    writer.save()
    writer.close()




