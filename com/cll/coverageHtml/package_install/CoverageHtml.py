import os
from bs4 import BeautifulSoup
import re
import pandas as pd
import tkinter as tk
import tkinter.messagebox

errorMessage = ""
fileDirectoryArr = []
def get_directory(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            sub_file = os.listdir(path)
            for file_name in sub_file:
                join_path = os.path.join(path, file_name)
                if os.path.isdir(join_path):
                    fileDirectoryArr.append(join_path)
        else:
            print("我要操作文件")
    else:
        errorMessage = "该文件路径不存在"
        print("该文件路径不存在")
        return errorMessage
    return fileDirectoryArr

#获取文件夹下所有的文件
# 返回路径下指定fileName
fileNameArr = []
def get_fileName(path, fileNameSuffix):
    try:
        if os.path.exists(path):
            if os.path.isdir(path):
                sub_file = os.listdir(path)
                for file_name in sub_file:
                    join_path = os.path.join(path, file_name)
                    if os.path.isfile(join_path):
                        if os.path.splitext(join_path)[-1] == fileNameSuffix:
                            print(join_path)
                            fileNameArr.append(join_path)
                    elif os.path.isdir(join_path):
                        get_fileName(join_path, fileNameSuffix)
            else:
                print("我要操作文件")
        else:
            errorMessage = "该文件路径不存在"
            print("该文件路径不存在")
            return errorMessage
        return fileNameArr
    except IOError as e:
        errorMessage = "该文件路径不存在"
        print("该文件路径不存在")
        return errorMessage

#读取数据，存放入元组
def read_file_getArrayData(file):
    with open(file, 'r', encoding='utf-8') as f:
        json_data_map = []
        json_data_map = f.readlines()
        json_map = {}
        count = 0
        for i in f:
            str = f.readline()
            #将结果放入Map中
            #json_map.setdefault(count,[]).append(str)
            json_map.setdefault(count, str)
            count = count + 1
        return json_data_map

#统计jcoco覆盖率的整合工具
def buttonFuntion():
    #path = "C:\\Users\\30270\\HBuilderProjects"
    path = inputString.get()
    #查找当前文件下的第一层级文件夹
    fileDirectoryArr = get_directory(path)
    isFirstConvter = True
    #判断是否输入正确的文件夹路径
    if type(fileDirectoryArr) is str:
        tk.messagebox.showerror(title='出错', message=fileDirectoryArr)
        fileDirectoryArr.clear()
        return
    for fileDirectory in fileDirectoryArr:
        #初始化
        #fileNameArr.clear()
        #w = 0代表生成sheet顺序
        w = 0
        #遍历当前文件下的第一层级文件夹下所有的html
        fileNameArr = get_fileName(fileDirectory, ".html")
        # 判断是否输入正确的文件夹路径
        if type(fileNameArr) is str:
            tk.messagebox.showerror(title='出错', message=fileNameArr)
            fileDirectoryArr.clear()
            fileNameArr.clear()
            return
        # 判断是否进行转换
        if isFirstConvter is True:
            result = tkinter.messagebox.askquestion(title='标题', message='你确定要进行转换')
            if result == 'no':
                result = tkinter.messagebox.showwarning(title='警号', message='你取消了转换操作')
                fileDirectoryArr.clear()
                fileNameArr.clear()
                return
            isFirstConvter = False
        excelName = fileDirectory[str(fileDirectory).rindex("\\")+1:]
        #创建excel的flg
        isWriterExcel = False
        #判断当前文件夹是否存在对象,存在isWriterExcel = True,并创建excel
        for file in fileNameArr:
            if str(file).endswith("index.html"):
                isWriterExcel = True
                break
        if isWriterExcel is True:
            #创建以第一层级文件夹Excel文件
            #mode='a'追加数据,mode='w'覆盖文件数据
            writer = pd.ExcelWriter(excelName + ".xlsx", mode='w', engine='openpyxl')
        for file in fileNameArr:
            if str(file).endswith("index.html"):
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
                    dateArr11["biaotou"] = ['序号', '项目名', 'java包名', '覆盖率']
                    #i = 0标记dateArr11中key不能重复
                    i = 0
                    sheetName = ""
                    #tbody.select('tr')查找tbody下所有的tr标签
                    for tbodyChildren in tbody.select('tr'):
                        #使用正则匹配当前tr标签中存在百分比
                        pattern = re.compile(r'(?<=>)(\d+%)(?=<)')
                        res = pattern.search(str(tbodyChildren))
                        if res != None and len(child_page.select('#breadcrumb a.el_bundle')) > 0:
                            #初始化,存放数据
                            dateArr = []
                            #添加序列
                            dateArr.append(i)
                            #获取项目名<td id="a0"><a href="App.html" class="el_class">App</a></td>
                            dateArr.append(child_page.select('#breadcrumb a.el_bundle')[0].string)
                            #child_page.title.string获取包名
                            #tbodyChildren.td.a.string获取class名
                            dateArr.append(child_page.title.string + '.' + tbodyChildren.td.a.string)
                            #获取覆盖率百分比
                            dateArr.append(res.group())
                            #设置sheet名字
                            sheetName = child_page.title.string
                            #将数据存放入字典
                            dateArr11[child_page.title.string + '.' + tbodyChildren.td.a.string + str(i)] = dateArr
                            i += 1
                    if len(sheetName) > 0:
                        #dateArr11数据格式, 如: {"col1": [1, 2, 3], "col2": [4, 5, 6], "col3": [7, 8, 9]}
                        #默认输出为竖向排列
                        #T代表可以将数据横向排列,输出表格中
                        data = pd.DataFrame(dateArr11).T
                        #写入数据
                        data.to_excel(writer, sheet_name=sheetName + str(w), index=False)
                        w += 1
        if isWriterExcel is True:
            #保存excel,并关闭
            writer.close()
            fileNameArr.clear()
    tk.messagebox.showinfo(title='信息提示！', message='转换完成!')

#画面UI
root = tk.Tk()

root.title("统计覆盖率")
#设置小图标
root.iconbitmap('vip.ico')
#设置窗口大小,窗口位置
root.geometry('1150x640+400+200')
#设置head图片
image = tk.PhotoImage(file='image/vip_s_1.png')
tk.Label(root, image=image).pack()

#设置输入框
input_frame = tk.LabelFrame(root)
input_frame.pack(fill='both', padx='5', pady='5', ipadx='5', ipady='5')
tk.Label(input_frame, text='请输入覆盖率文件路径:', background='#f0f0f0', font=('黑体', 20), padx='8', pady='2',).pack(side=tk.LEFT)
inputString = tk.StringVar()
tk.Entry(input_frame, textvariable=inputString, width='200', relief='flat', font=('黑体', 12)) .pack(side=tk.LEFT, fill='both')

#设置按钮
#relief='flat'设置平滑
#按钮绑定事件command=buttonFuntion
button = tk.Button(root, command=buttonFuntion,
                   text='Go-点击生成覆盖率统计', font=('黑体', 12), background='#5cb85c', wraplength='200', relief='flat')
button.config(fg='white')
button.pack(fill='both', padx='8', pady='2')

root.mainloop()


