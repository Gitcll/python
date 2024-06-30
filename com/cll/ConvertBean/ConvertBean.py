import re
import tkinter as tk
from configparser import ConfigParser
from tkinter import ttk


def static_div():
    package = '''/*
 * qwe-web - {}.java
 *
 * qwe Package.
 *
 * Copyright (C) 
 */'''

    class_comment_code = """/**
 * {}
 *
 * <pre>
 * The persistent class for the {} database table.
 * </pre>
 *
 * @author qwe
 */"""

    class_pk_comment_code = """/**
 * {}PKクラス
 *
 * <pre>
 * {}PKクラス
 * </pre>
 *
 * @author qwe
 */"""

    class_code = '''@Entity
@Table(name="{}")
@NamedQuery(name="{}.findAll", query="SELECT m FROM {} m")
public class {} implements Serializable {{'''

    class_pk_code = '''@Embeddable
public class {} implements Serializable {{'''

    field_serializable_code = '''    /**
     * serialVersionUID.
     */
    private static final long serialVersionUID = 1L;'''

    field_pk_code = '''    /**
     * {}PKクラス
     */
    @EmbeddedId
    private {}PK {}PK;'''

    field_code = '''    /**
     * {}
     */
    @Column(name = "{}")
    private {} {};'''

    get_method_code = '''    /**
     * {}を取得する
     *
     * @return {} {}
     */
    public {} get{}() {{

        return {};
    }}'''

    set_method_code = '''    /**
     * {}を設定する
     *
     * @param {}
     *            {}
     */
    public void set{}({} {}) {{

        this.{} = {};
    }}'''
    return package, class_comment_code, class_code, class_pk_comment_code, class_pk_code, field_serializable_code, field_pk_code, field_code, get_method_code, set_method_code


def convert_to_camel_case(text):
    # 将下划线分隔的单词转换为首字母大写的驼峰命名
    words = text.split('_')
    camel_case = ''.join([word.capitalize() for word in words])
    return camel_case


def create_primary_key_method(primary_key_dict, className, table_comment):
    write_arr = []
    classNamePK = className + "PK"
    package, class_comment_code, class_code, \
        class_pk_comment_code, class_pk_code, \
        field_serializable_code, field_pk_code, \
        field_code, get_method_code, set_method_code = static_div()

    package = package.format(classNamePK)
    write_arr.append(package)

    class_pk_comment_code = class_pk_comment_code.format(table_comment, table_comment)
    write_arr.append(class_pk_comment_code)

    class_pk_code = class_pk_code.format(classNamePK)
    write_arr.append(class_pk_code)

    write_arr.append(field_serializable_code)
    for key, value in primary_key_dict.items():
        setget = value[1]
        field_comment = value[2]
        field_type = value[3]

        field_type = CONFIG_INFO[field_type]
        if field_type is None:
            field_type = "请将" + value[1] + "添加到config.ini配置中：" + value[1] + "=对应javaType"
        field_var = setget[0].lower() + setget[1:]
        field_code_str = field_code.format(field_comment, key, field_type, field_var)
        write_arr.append(field_code_str)

    for key, value in primary_key_dict.items():
        setget = value[1]
        field_comment = value[2]
        field_type = value[3]
        if field_type is None:
            field_type = "请将" + value[1] + "添加到config.ini配置中：" + value[1] + "=对应javaType"

        field_var = setget[0].lower() + setget[1:]
        get_method_code_str = get_method_code.format(field_comment, field_var, field_comment, field_type, setget,
                                                     field_var)
        set_method_code_str = set_method_code.format(field_comment, field_var, field_comment, setget, field_type,
                                                     field_var, field_var, field_var)
        write_arr.append(get_method_code_str)
        write_arr.append(set_method_code_str)

    write_arr.append("}")
    if write_arr:
        with open(classNamePK + ".java", "w", encoding="UTF-8") as file:
            for write_value in write_arr:
                file.write(write_value + "\n\n")


def submit():
    values = text_box.get("1.0", "end-1c").split("\n")  # 获取文本框中的所有值，并按行分割
    values = [value.strip() for value in values if value.strip()]  # 去除空行并去除首尾空格

    package, class_comment_code, class_code, \
        class_pk_comment_code, class_pk_code, \
        field_serializable_code, field_pk_code, \
        field_code, get_method_code, set_method_code = static_div()

    taulus_dict = {}
    field_dict = {}
    table_arr = []
    primary_key_dict = {}
    write_arr = []
    values[0] = "Table\t" + values[0]
    for element in values:
        split = element.split("\t")
        if split[0] == "Table":
            table_name = split[2]
            table_comment = split[1]
            className = convert_to_camel_case(table_name)
            table_name_upper = table_name.upper()
            table_arr = [table_name, table_comment, className, table_name_upper]

            if len(split) == 4:
                primary_name = split[3]
                primary_key_dict[primary_name] = table_name
            else:
                primary_name1 = split[3]
                primary_name2 = split[4]
                primary_key_dict[primary_name1] = table_name
                primary_key_dict[primary_name2] = table_name
            continue
        # taulus_dict
        key = split[1]
        value2 = split[2]
        if value2.startswith("numeric"):
            if "," in value2:
                sub = "numeric1"
            else:
                sub = "numeric2"
        else:
            sub = re.sub("\(.*", "", value2)
        value = [split[0], sub]
        taulus_dict[key] = value

        # field_dict #
        upper = split[1].lower()
        case = convert_to_camel_case(split[1])
        value = [upper, case]
        field_dict[key] = value

    table_name = table_arr[0]
    table_comment = table_arr[1]
    className = table_arr[2]
    table_name_upper = table_arr[3]
    package = package.format(className)
    write_arr.append(package)

    class_comment_code = class_comment_code.format(table_comment, table_name_upper)
    write_arr.append(class_comment_code)

    class_code = class_code.format(table_name, className, className, className)
    write_arr.append(class_code)

    write_arr.append(field_serializable_code)
    if len(primary_key_dict) == 2:
        classNameFirstLower = className[0].lower() + className[1:]
        field_pk_code = field_pk_code.format(table_arr[1], className, classNameFirstLower)
        write_arr.append(field_pk_code)

        for key, value in primary_key_dict.items():
            field_get = field_dict.get(key)
            taulus_get = taulus_dict.get(key)
            if field_get is not None and taulus_get is not None:
                field_get.append(taulus_get[0])
                field_get.append(taulus_get[1])
                primary_key_dict[key] = field_get

        create_primary_key_method(primary_key_dict, className, table_comment)

    for key, value in taulus_dict.items():
        field_value = field_dict[key]
        field_type = CONFIG_INFO[value[1]]
        if field_type is None:
            field_type = "请将" + value[1] + "添加到config.ini配置中：" + value[1] + "=对应javaType"

        field_var = field_value[1][0].lower() + field_value[1][1:]
        field_code_str = field_code.format(value[0], field_value[0], field_type, field_var)

        if len(primary_key_dict) == 1 and primary_key_dict.get(key) is not None:
            field_code_str = field_code_str.replace("@Column", "@Id\n    @Column")
            write_arr.append(field_code_str)
        else:
            write_arr.append(field_code_str)

    for key, value in taulus_dict.items():
        field_value = field_dict[key]
        field_type = CONFIG_INFO[value[1]]
        if field_type is None:
            field_type = "请将" + value[1] + "添加到config.ini配置中：" + value[1] + "=对应javaType"

        field_var = field_value[1][0].lower() + field_value[1][1:]
        get_method_code_str = get_method_code.format(value[0], field_var, value[0], field_type, field_value[1],
                                                     field_var)
        set_method_code_str = set_method_code.format(value[0], field_var, value[0], field_value[1], field_type,
                                                     field_var, field_var, field_var)
        write_arr.append(get_method_code_str)
        write_arr.append(set_method_code_str)

    write_arr.append("}")
    if write_arr:
        with open(className + ".java", "w", encoding="UTF-8") as file:
            for write_value in write_arr:
                file.write(write_value + "\n\n")


# 读取配置文件
config = ConfigParser()
config.read('config.ini', encoding="UTF-8")
CONFIG_INFO = {}
for k, v in config['Config'].items():
    CONFIG_INFO[k] = v.replace("\"\"\"", "").replace("\\n", "\n")

# 创建根窗口
root = tk.Tk()
root.title("ConvertBean")

# 设置窗口大小和背景颜色
window_width = 800
window_height = 500
root.geometry(f"{window_width}x{window_height}")  # 设置窗口大小为宽400像素，高300像素
root.configure(bg="#f0f0f0")  # 设置窗口背景颜色为浅灰色

# 创建文本框
text_box_width = window_width // 8  # 设置文本框宽度为窗口宽度的1/20
text_box_height = window_height // 20  # 设置文本框高度为窗口高度的1/30
text_box = tk.Text(root, width=text_box_width, height=text_box_height, bg="white")  # 设置文本框背景颜色为白色
text_box.grid(row=0, column=0, padx=10, pady=10)

# 创建提交按钮
button_style = ttk.Style()
button_style.configure("TButton", font=("Arial", 12), background="#4CAF50", foreground="white", padding=10,
                       borderwidth=0, relief="flat", width=20, bordercolor="#4CAF50", focuscolor="#81C784")
submit_button = ttk.Button(root, text="提交", command=submit, style="TButton")  # 设置按钮样式
submit_button.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()
