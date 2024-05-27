import os
import re
from tkinter import *
from typing import Dict
from collections import OrderedDict

import cchardet
from ttkbootstrap import *
import tkinter.messagebox as messagebox
import time
from datetime import datetime


class WinGUI(Tk):
    widget_dic: Dict[str, Widget] = {}

    def __init__(self):
        super().__init__()
        self.__win()
        self.widget_dic["tk_label_log_path"] = self.__tk_label_log_path(self)
        self.widget_dic["tk_input_log_path"] = self.__tk_input_log_path(self)
        self.widget_dic["tk_label_filter_string"] = self.__tk_label_filter_string(self)
        self.widget_dic["tk_input_filter_string"] = self.__tk_input_filter_string(self)
        self.widget_dic["tk_label_start_time"] = self.__tk_label_start_time(self)
        self.widget_dic["tk_input_start_time"] = self.__tk_input_start_time(self)
        self.widget_dic["tk_label_dateformat"] = self.__tk_label_dateformat(self)
        self.widget_dic["tk_input_dateformat"] = self.__tk_input_dateformat(self)
        self.widget_dic["tk_label_pattern"] = self.__tk_label_pattern(self)
        self.widget_dic["tk_input_pattern"] = self.__tk_input_pattern(self)
        self.widget_dic["tk_label_out_path"] = self.__tk_label_out_path(self)
        self.widget_dic["tk_input_out_path"] = self.__tk_input_out_path(self)
        self.widget_dic["tk_button_active"] = self.__tk_button_active(self)
        self.widget_dic["tk_label_copyright"] = self.__tk_label_copyright(self)

    def __win(self):
        self.title("SQL抽取")
        # 设置窗口大小、居中
        width = 586
        height = 400
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

        # 自动隐藏滚动条

    def scrollbar_autohide(self, bar, widget):
        self.__scrollbar_hide(bar, widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))

    def __scrollbar_show(self, bar, widget):
        bar.lift(widget)

    def __scrollbar_hide(self, bar, widget):
        bar.lower(widget)

    def __tk_label_log_path(self, parent):
        label = Label(parent, text="SQL Log 路径：", anchor="center", )
        label.place(x=30, y=10, width=87, height=30)
        return label

    def __tk_input_log_path(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=120, y=10, width=425, height=30)
        return ipt

    def __tk_label_filter_string(self, parent):
        label = Label(parent, text="过滤关键字：", anchor="center", )
        label.place(x=30, y=60, width=89, height=30)
        return label

    def __tk_input_filter_string(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=120, y=60, width=424, height=30)
        return ipt

    def __tk_label_out_path(self, parent):
        label = Label(parent, text="SQL输出路径：", anchor="center", )
        label.place(x=30, y=110, width=87, height=30)
        return label

    def __tk_input_out_path(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=120, y=110, width=425, height=30)
        return ipt

    def __tk_label_start_time(self, parent):
        label = Label(parent, text="操作时间：", anchor="center", )
        label.place(x=25, y=160, width=87, height=30)
        return label

    def __tk_input_start_time(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=120, y=160, width=425, height=30)
        return ipt

    def __tk_label_dateformat(self, parent):
        label = Label(parent, text="操作时间格式：\n(%d/%m/%Y %H:%M:%S:%f)", anchor="center", )
        label.place(x=0, y=215, width=230, height=50)
        return label

    def __tk_input_dateformat(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=120, y=210, width=425, height=30)
        return ipt

    def __tk_label_pattern(self, parent):
        label = Label(parent, text="操作时间正则：", anchor="center", )
        label.place(x=-40, y=260, width=230, height=50)
        return label

    def __tk_input_pattern(self, parent):
        ipt = Entry(parent, )
        ipt.place(x=120, y=260, width=425, height=30)
        return ipt

    def __tk_button_active(self, parent):
        btn = Button(parent, text="开始抽取", takefocus=False, )
        btn.place(x=260, y=310, width=79, height=30)
        return btn

    def __tk_label_copyright(self, parent):
        label = Label(parent, text="Copyright © SOFTROAD. All rights reserved.", anchor="center", )
        label.place(x=160, y=350, width=297, height=30)
        return label

class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()

    # 获取文件编码类型
    def get_encoding_cchardet(self, file):
        # 二进制方式读取，获取字节数据，检测类型
        with open(file, 'rb') as f:
            return cchardet.detect(f.read())['encoding']

    def sql_check_out(self, env):
        log_path = self.widget_dic["tk_input_log_path"].get()
        #log_path = "F:\SVN\Tool\log1"
        if not all([log_path]):
            messagebox.showerror("Warning", "请输入log文件路径！")
            return

        filter_string = self.widget_dic["tk_input_filter_string"].get()
        #filter_string = "192.168.8.163"
        if not all([filter_string]):
            messagebox.showerror("Warning", "请输入过滤关键字！")
            return

        out_path = self.widget_dic["tk_input_out_path"].get()
        #out_path = "F:/SVN/Tool"
        if not all([out_path]):
            messagebox.showerror("Warning", "请输入SQL输出路径！")
            return

        start_time = self.widget_dic["tk_input_start_time"].get()
        #start_time = "09/10/2023 10:27:35:724"
        #start_time = "2023/10/09 17:39:26.065"
        if not all([start_time]):
            messagebox.showerror("Warning", "请输入操作开始时间，例如：2023-06-20 09:34:13,485")
            return

        date_format = self.widget_dic["tk_input_dateformat"].get()
        #date_format = "%d/%m/%Y %H:%M:%S:%f"
        #date_format = "%Y/%m/%d %H:%M:%S.%f"
        if not all([date_format]):
            messagebox.showerror("Warning", "请输入操作开始时间，例如：%d/%m/%Y %H:%M:%S:%f\n"
                                            "%d: 表示两位数的日期，范围是01到31。\n"
                                            "%m: 表示两位数的月份，范围是01到12。\n"
                                            "%Y: 表示四位数的年份，例如2023。\n"
                                            "%H: 表示24小时制的小时，范围是00到23。\n"
                                            "%M: 表示分钟，范围是00到59。\n"
                                            "%S: 表示秒数，范围是00到59。\n"
                                            "%f: 表示微秒（小数部分），范围是000000到999999。在这个格式中，只会保留三位数字的微秒。")
            return

        pattern = self.widget_dic["tk_input_pattern"].get()
        #pattern = "\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}:\d{3}"
        #pattern = "\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}.\d{3}"
        if not all([pattern]):
            messagebox.showerror("Warning", "请输入操作时间正则表达式，例如：\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}:\d{3}")
            return

        try:
            log_files = [f for f in os.listdir(log_path) if os.path.isfile(os.path.join(log_path, f))]
            # 根据日期和时间拼接文件名
            action_date_time = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
            export_path = out_path + '\\' + action_date_time + '_sql_queries.txt'
            with open(export_path, 'w', encoding='utf-8') as output_file:
                dateArr11 = {}
                for log_file in log_files:
                    log_file_path = os.path.join(log_path, log_file)
                    with open(log_file_path, 'r', encoding='cp932') as log:
                        if len(start_time) > 0:
                            is_begin = False
                        else:
                            is_begin = True
                        for line in log:
                            pattern = re.compile(pattern)
                            res = pattern.search(str(line))
                            if res != None:
                                matched_time = res.group()
                                if line.find(start_time) > -1 or is_begin:
                                    is_begin = True
                                    if dateArr11.__contains__(matched_time):
                                        get = dateArr11.get(matched_time)
                                        get.append(line)
                                    else:
                                        date_stringsArr = []
                                        date_stringsArr.append(line)
                                        dateArr11[matched_time] = date_stringsArr
                            else:
                                print("No match found:  " + line + "\n")

                # 将日期时间字符串转换为datetime对象并存储到OrderedDict中
                ordered_dict = OrderedDict()
                for key in sorted(dateArr11.keys(), key=lambda x: datetime.strptime(x, date_format)):
                    ordered_dict[key] = dateArr11[key]

                split = filter_string.split(";")

                # 连续输出值
                for value in ordered_dict.values():
                    for line in value:
                        for filterStr in split:
                            strip = filterStr.strip()
                            if line.find(strip) != -1:
                                output_file.write(line)

                # 保存文件
                output_file.close()
            messagebox.showinfo(title='Info', message='successful!')
        except Exception as e:
            messagebox.showerror("Exception", e)

    def __event_bind(self):
        self.widget_dic["tk_button_active"].bind('<Button>', self.sql_check_out)


if __name__ == "__main__":
    win = Win()
    win.mainloop()
