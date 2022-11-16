from com.cll.io.FileIO import *
from com.cll.io.commFile import *
from bs4 import BeautifulSoup
import re
from com.cll.excel.Xlsxwriter import *
import pandas as pd


path = "C:\\Users\\30270\\HBuilderProjects"
fileDirectoryArr = get_directory(path)
print(fileNameArr)
for fileDirectory in fileDirectoryArr:
    fileNameArr = get_fileName(fileDirectory, ".html")
    print(fileNameArr)
    w = 0
    for file in fileNameArr:
        if str(file).endswith("index.html"):
            print(file)
            date = read_file_getArrayData(file)
            child_page = BeautifulSoup(str(date), "html.parser")
            tbody = child_page.find("tbody")
            if tbody != None:
                dateArr11 = []
                for tbodyChildren in tbody.select('tr'):
                    print(tbodyChildren)
                    pattern = re.compile(r'(?<=>)(\d+%)(?=<)')
                    res = pattern.search(str(tbodyChildren))
                    if res != None:
                        dateArr = []
                        #获取<td id="a0"><a href="App.html" class="el_class">App</a></td>
                        dateArr.append(child_page.select('#breadcrumb a.el_bundle')[0].string)
                        dateArr.append(child_page.title.string + '.' + tbodyChildren.td.a.string)
                        dateArr.append(res.group())
                        dateArr11.append(dateArr)
                print(dateArr11)
                fileName = '测试.xlsx'
                xw_toExcel(dateArr11, fileName, str(tbody.name)+str(w))
                w += 1
                p = 2;
                for date_ in dateArr11:
                    data = pd.DataFrame(date_).T
                    writer = pd.ExcelWriter("excel 样例.xlsx", mode='a', engine='openpyxl')
                    data.to_excel(writer, sheet_name="这是第1个sheet",index=False)
                writer.save()
                writer.close()



