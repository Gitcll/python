from com.cll.io.FileIO import *
from com.cll.io.commFile import *
from bs4 import BeautifulSoup
import re
from com.cll.excel.Xlsxwriter import *


path = "D:\Java"
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
                for tbodyChildren in tbody.children:
                    print(tbodyChildren)
                    pattern = re.compile(r'(?<=>)\w+(\.\w+){0,}(?=<)')
                    res = pattern.search(str(tbodyChildren))
                    if res != None:
                        dateArr = []
                        dateArr.append(res.group())
                        dateArr11.append(dateArr)
                print(dateArr11)
                fileName = '测试.xlsx'
                xw_toExcel(dateArr11, fileName, str(tbody.name)+str(w))
                w += 1


