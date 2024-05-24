import os
import re
import threading
import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import filedialog
import tkinter.messagebox
import cchardet
import shutil
from pathlib import Path

class FileConvter:
    def __init__(self):
        pass

    # 获取文件编码类型
    def get_encoding_cchardet(self, file):
        # 二进制方式读取，获取字节数据，检测类型
        with open(file, 'rb') as f:
            encoding = cchardet.detect(f.read())['encoding']
            if encoding.upper() == 'SHIFT_JIS':
                encoding = 'cp932'
            return encoding

    def prepend_slash_or_backslash(self, line):
        """
        如果字符串line的开头没有 '\' 或 '/'，则检查字符串中是否存在这些字符，
        并在第一个发现的 '\' 或 '/' 前面追加相应符号。
        """
        if not line.startswith('\\') or not line.startswith('/'):
            if line.find('\\') == -1:
                line = '\\' + line
            else:
                line = '/' + line
        return line

    def ensure_directory_clean(self, path):
        """
        确保目录存在并干净（如果已存在则先删除再创建）。
        """
        if os.path.exists(path):
            # 如果目录存在，则先删除
            shutil.rmtree(path)
        # 创建新目录
        os.makedirs(path, exist_ok=True)

    def isFileExists(self, inputPathEntry, outputTimeDirEntry, outputTimeDirText, fileNameArr, outFileNameMap):
        try:
            temp = ""
            if len(outputTimeDirEntry) > 0 and os.path.isdir(outputTimeDirEntry):
                temp = outputTimeDirEntry
            else:
                temp = "C:\\CopyFileTemp"
            self.ensure_directory_clean(temp)
            # 使用splitlines()方法将文本按行分割成列表
            lines_list = outputTimeDirText.splitlines()

            if os.path.exists(inputPathEntry):
                if os.path.isdir(inputPathEntry):
                    # 遍历列表
                    for line in lines_list:
                        # 对每一行进行处理，比如打印出来
                        line = self.prepend_slash_or_backslash(line)
                        join_path = os.path.join(inputPathEntry + line)
                        if os.path.isfile(join_path):
                            dirname = os.path.dirname(line)
                            basename = os.path.basename(line)

                            outFileNameMap[join_path] = temp + dirname + "\t" + basename
                            fileNameArr.append(join_path)
                        else:
                            print('查看文件路径是否正确:' + join_path)
                            tk.messagebox.showwarning(title='详细信息查看控制台', message='查看文件路径是否正确:' + join_path)
                else:
                    print('当前路径不正:' + inputPathEntry)
                    tk.messagebox.showwarning(title='详细信息查看控制台', message='当前路径不正:' + join_path)
            else:
                print('当前路径不存在:' + inputPathEntry)
                tk.messagebox.showwarning(title='详细信息查看控制台', message='当前路径不存在:' + join_path)
        except IOError as e:
            ExceptionConvter(e, '文件解析失败').errorException()

class FileCopyOrMoveMain:
    def __init__(self, inputPathEntry, outputTimeDirEntry, outputTimeDirText, num_int_va_):
        self.inputPathEntry = inputPathEntry
        self.outputTimeDirEntry = outputTimeDirEntry
        self.outputTimeDirText = outputTimeDirText
        self.num_int_va_ = num_int_va_
        if self.num_int_va_ == 1:
            print("Initializing CopyFile Start...")
        elif self.num_int_va_ == 2:
            print("Initializing MoveFile Start...")
    def main(self):
        try:
            fileNameArr = []
            outFileNameMap = {}
            FileConvter().isFileExists(self.inputPathEntry, self.outputTimeDirEntry, self.outputTimeDirText, fileNameArr, outFileNameMap)
            if len(fileNameArr) > 0:
                for fielLine in fileNameArr:
                    get = outFileNameMap.get(fielLine)
                    split = str(get).split("\t")
                    os.makedirs(split[0], exist_ok=True)
                    pathout = Path(split[0]).resolve() / split[1]
                    if self.num_int_va_ == 1:
                        shutil.copy2(fielLine, pathout)
                    elif self.num_int_va_ == 2:
                        shutil.move(fielLine, pathout)
                    print("CopyFile End ... Success\t" + str(pathout))
                tk.messagebox.showwarning(title='Warning', message='提取文件成功!!!')
            else:
                tk.messagebox.showwarning(title='Warning', message='未获取到指定文件或者指定文件不存在')
        except IOError as e:
            ExceptionConvter(e, '提取文件失败').errorException()

class ExceptionConvter:
    def __init__(self, exption, message):
        self.exption = exption
        self.message = message

    def errorException(self):
        efilename = ""
        if self.exption.filename != None:
            efilename = "文件路径: " + self.exption.filename + "\n"
        estrerror = ""
        if self.exption.strerror != None:
            estrerror = "错误原因: " + self.exption.strerror + "\n"
        ewinerror = ""
        if self.exption.winerror != None:
            ewinerror = "错误原因: " + self.exption.winerror + "\n"
        print(self.message + '\n' + estrerror + ewinerror + efilename)
        tk.messagebox.showerror(title='error', message=self.message + '\n' + estrerror + ewinerror + efilename)

class FileManager:
    def __init__(self, master):
        self.master = master
        master.title("从一个源路径提取指定的文件到一个新的目标路径")
        master.geometry('1150x640+400+200')

        # 请输入源文件夹路径输入框
        input_frame = tk.LabelFrame(master)
        input_frame.pack(fill='both', padx='5', pady='5', ipadx='5', ipady='5')
        tk.Label(input_frame, text='请输入源文件夹路径:', background='#f0f0f0', font=('黑体', 20), padx='8',
                 pady='2', ).pack(side=tk.LEFT)
        inputString = tk.StringVar(value='')
        self.inputPathEntry = tk.Entry(input_frame, textvariable=inputString, width='200', relief='flat', font=('黑体', 12))
        self.inputPathEntry.pack(side=tk.LEFT, fill='both')

        # 请输出新的目标文件夹路径输入框
        output_pathDir_frame = tk.LabelFrame(master)
        output_pathDir_frame.pack(fill='both', padx='5', pady='5', ipadx='5', ipady='5')
        tk.Label(output_pathDir_frame, text='请输入新的目标文件夹路径:', background='#f0f0f0', font=('黑体', 20), padx='8',
                 pady='2', ).pack(side=tk.LEFT)
        outputTimeDirString = tk.StringVar(value='')
        self.outputTimeDirEntry = tk.Entry(output_pathDir_frame, textvariable=outputTimeDirString, width='200',
                                           relief='flat', font=('黑体', 12))
        self.outputTimeDirEntry.pack(side=tk.LEFT, fill='both')

        # 请输出指定的文件路径输入框
        output_timeDir_frame = tk.LabelFrame(master)
        output_timeDir_frame.pack(fill='both', padx='5', pady='5', ipadx='5', ipady='5')
        tk.Label(output_timeDir_frame, text='请输入指定的文件路径:', background='#f0f0f0', font=('黑体', 20), padx='8',
                 pady='2').pack(side=tk.LEFT)
        # 修改为Text组件以支持多行输入
        self.outputTimeDirText = tk.Text(output_timeDir_frame, height=5, width=40, relief='flat',
                                         font=('黑体', 12), wrap='word')  # 设置高度、宽度和自动换行
        self.outputTimeDirText.pack(side=tk.LEFT, fill='both', expand=True)  # 使用fill和expand使其填充空间并可扩展

        # 设置fram框
        choose_frame = tk.LabelFrame(master)
        choose_frame.pack(fill='both', padx='5', pady='5', ipadx='5', ipady='5')
        tk.Label(choose_frame, text='选择类型:', background='#f0f0f0', font=('黑体', 20), padx='8', pady='2', ).pack(side=tk.LEFT)
        self.num_int_va = tk.IntVar()
        self.num_int_va.set(1)
        radiobutton = tk.Radiobutton(choose_frame, text='.copy', font=('黑体', 12), padx='5', pady='2',
                                     variable=self.num_int_va, value=1).pack(side=tk.LEFT)
        radiobutton = tk.Radiobutton(choose_frame, text='.move', font=('黑体', 12), padx='5', pady='2',
                                     variable=self.num_int_va, value=2).pack(side=tk.LEFT)

        # 选择输入源文件夹路径按钮
        button = tk.Button(master, command=self.open_input_file,
                           text='选择输入源文件夹路径', font=('黑体', 12), background='#5cb85c', wraplength='200', relief='flat')
        button.config(fg='white')
        button.pack(fill='both', padx='8', pady='2')

        # 选择输出新的目标文件夹路径按钮
        button = tk.Button(master, command=self.open_output_file,
                           text='选择输入新的目标文件夹路径(可选)', font=('黑体', 12), background='#ace04a', wraplength='200', relief='flat')
        button.config(fg='white')
        button.pack(fill='both', padx='8', pady='2')

        # 输出结果按钮
        button = tk.Button(master, command=self.result,
                           text='输出结果', font=('黑体', 12), background='#55b8bf', wraplength='200', relief='flat')
        button.config(fg='white')
        button.pack(fill='both', padx='8', pady='2')

        # 说明文档
        textExplain = tk.Text(root, bg='#f0efeb', fg='red', font=('黑体', 20))
        textExplain.insert("1.0", "1.请输入源文件夹路径,必填项\n")
        textExplain.insert("2.0", "2.请输出新的目标文件夹路径,默认路径「C:\CopyFileTemp」,非必填项\n")
        textExplain.insert("3.0", "3.请输出指定的文件路径,必填项\n"
                                  "    需要提取文件路径格式为：\n"
                                  "    ① path1\path2\\filename.*\n"
                                  "    ②\path1\path2\\filename.*\n"
                                  "    ③ path1/path2/filename.*\n"
                                  "    ④/path1/path2/filename.*\n")
        textExplain.pack()

    def open_input_file(self):
        file_path = filedialog.askdirectory(parent=self.master, title="请输入文件夹")
        if file_path:
            self.inputPathEntry.delete(0, tk.END)
            self.inputPathEntry.insert(0, file_path)

    def open_output_file(self):
        if len(self.inputPathEntry.get()) > 0:
            file_path = filedialog.askdirectory(parent=self.master, title="请输出文件夹")
            if file_path:
                self.outputTimeDirEntry.delete(0, tk.END)
                self.outputTimeDirEntry.insert(0, file_path)
        else:
            tk.messagebox.showwarning(title='Warning', message='「选择输入源文件夹路径」不能为空')


    def resultThread(self):
        self.thread = threading.Thread(target=self.result)
        # 启动线程
        self.thread.start()

    def result(self):
        inputPathEntry = self.inputPathEntry.get()
        outputTimeDirEntry = self.outputTimeDirEntry.get()
        if len(inputPathEntry) > 0:
            outputTimeDirText = self.outputTimeDirText.get("1.0", tk.END)
            if len(outputTimeDirText) > 1:
                num_int_va_ = self.num_int_va.get()
                FileCopyOrMoveMain(inputPathEntry, outputTimeDirEntry, outputTimeDirText, num_int_va_).main()
            else:
                tk.messagebox.showwarning(title='Warning', message='「请输入指定的文件路径」不能为空')
        else:
            tk.messagebox.showwarning(title='Warning', message='「选择输入源文件夹路径」不能为空')

if __name__ == "__main__":
    root = tk.Tk()
    fm = FileManager(root)
    root.mainloop()
