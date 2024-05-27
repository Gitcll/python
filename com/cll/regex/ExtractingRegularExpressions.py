import tkinter as tk
import re

class RegexMatcher:
    def __init__(self, master):
        self.master = master
        master.title("Regex Matcher")

        # 创建正则表达式输入框
        self.regex_label = tk.Label(master, text="Regex:")
        self.regex_label.grid(row=0, column=0)

        self.regex_entry = tk.Entry(master, width=80)
        self.regex_entry.grid(row=0, column=1)

        # 创建文本输入框
        # 创建文本输入框
        self.text_label = tk.Label(master, text="Text:")
        self.text_label.grid(row=1, column=0)

        self.text_entry = tk.Text(master, height=17, width=130)
        self.text_entry.grid(row=1, column=1)

        # 创建匹配按钮
        self.match_button = tk.Button(master, text="Match", command=self.match)
        self.match_button.grid(row=2, column=0)

        # 创建去重复复选框
        self.distinct_var = tk.IntVar()
        self.distinct_checkbutton = tk.Checkbutton(master, text="Distinct", variable=self.distinct_var)
        self.distinct_checkbutton.grid(row=2, column=1)

        # 创建输出标签和文本框
        self.output_label = tk.Label(master, text="Output:")
        self.output_label.grid(row=3, column=0)

        self.output_text = tk.Text(master, height=17, width=130)
        self.output_text.grid(row=3, column=1)

    def match(self):
        # 获取用户输入的正则表达式和文本字符串
        regex = self.regex_entry.get()
        text = self.text_entry.get("1.0", tk.END)

        # 根据复选框的状态进行匹配和去重复
        if self.distinct_var.get():
            matches = list(set(re.findall(regex, text, flags=re.IGNORECASE)))
        else:
            matches = re.findall(regex, text, flags=re.IGNORECASE)

        # 在输出文本框中显示结果
        self.output_text.delete('1.0', tk.END)

        # 编译正则表达式
        compiled_regex = re.compile(regex)
        # 访问并打印分组数量
        num_groups = compiled_regex.groups
        if num_groups == 1:
            self.output_text.insert('1.0', '\n'.join(matches))
        else:
            output_string = ""
            for matche in matches:
                # 使用join方法将元组的每个元素用制表符连接起来，并在最后添加换行符
                output_string += "\t".join(map(str, matche)) + "\n"
            self.output_text.insert('1.0', output_string)



root = tk.Tk()
root.geometry('1150x640+400+200')
app = RegexMatcher(root)
root.mainloop()
