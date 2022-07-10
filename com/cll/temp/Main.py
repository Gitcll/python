from com.cll.temp.SeachKeyAndVale import *
from com.cll.io.commFile import *

fileDirName = "C:\\Users\\30270\\Desktop\\temp"
#存放txt数据
arrayDate = []
#定义字典元素
mapData = {}
#定义返回文件夹下所有的.txt文件
fileNameDate = []
fileNameDate = get_fileName(fileDirName, ".txt")

for fileName in fileNameDate:
    arrayDate = read_file_getArrayData(fileName)
    #将数据放入字典当中
    for str in arrayDate:
        strArr = str.split("|")
        if(len(strArr) > 0):
            mapData.setdefault(strArr[1].strip(), strArr[0].strip())

#控制台输入
a = input("请输入ID：")
if a.isdigit() is True:
    #通过key查询字典Value
    print("\r\n查询结果："+mapData.get(a))