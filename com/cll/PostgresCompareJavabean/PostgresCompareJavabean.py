
import os
import tkinter as tk
from tkinter import ttk
import psycopg2
from configparser import ConfigParser
import javalang
from javalang.tree import *

class JavaASTParser:
    def __init__(self, filename, tablescolumns_dict):
        self.filename = filename
        self.tablescolumns_dict = tablescolumns_dict

    def parse(self):
        try:
            with open(self.filename, 'r', encoding="UTF-8") as file:
                java_code = file.read()
                tree = javalang.parse.parse(java_code)
                self.process_tree(tree)
        except FileNotFoundError:
            print(f"File {self.filename} not found.")
        except javalang.parser.JavaSyntaxError as e:
            print(f"Syntax error in {self.filename}: {e}")

    def process_tree(self, tree):
        for path, node in tree:
            if isinstance(node, ClassDeclaration):
                self.process_class(node)

    def process_class(self, class_node):
        annotations = class_node.annotations
        if annotations:
            for annotation in annotations:
                if isinstance(annotation, Annotation):
                    if annotation.name == 'Table':
                        if class_node.extends:
                            parent_class_name = class_node.extends.name
                        table_name = str(annotation.element[0].value.value).replace("\"", "")
                        tablescolumns_dict = self.tablescolumns_dict
                        if tablescolumns_dict.get(table_name) is not None:
                            tablescolumns = tablescolumns_dict.get(table_name)
                            self.process_fields(class_node, table_name, tablescolumns)

    def process_fields(self, class_node, table_name, tablescolumns):
        fields = class_node.fields
        if fields:
            for field in fields:
                if isinstance(field, FieldDeclaration):
                    if len(field.annotations) > 0:
                        fieldAnnotations = field.annotations[0]
                        if fieldAnnotations.name == 'Column':
                            columnValue = fieldAnnotations.element[0].value.value.replace("\"", "").lower()
                            if tablescolumns.get(columnValue) is not None:
                                del tablescolumns[columnValue]
                            else:
                                notfindcolumn = "未匹配到数据库Column\t" + self.filename + "\t" + columnValue
                                classcolumnsnotfindpostgres.append(notfindcolumn)
            for str in tablescolumns:
                notfindcolumn = "未匹配到JavaBeanColumn\t" + self.filename + "\t" + table_name + "\t" + str
                postgrescolumnsnotfindclass.append(notfindcolumn)

    def get_table_name(self, annotation_node):
        for member in annotation_node.element_value_pairs:
            if member.name == 'name':
                return member.value.value
        return None


class PostgreSQLConnector:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connected to PostgreSQL database successfully!")
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection to PostgreSQL database closed.")

    def execute_query(self, query):
        if not self.connection:
            print("Error: Connection to database is not established.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            return None

def getPostgresConnect():
    try:
        # Example usage:
        connector = PostgreSQLConnector(
            dbname=CONFIG_INFO.get("dbname"),
            user=CONFIG_INFO.get("user"),
            password=CONFIG_INFO.get("password"),
            host=CONFIG_INFO.get("host"),
            port=CONFIG_INFO.get("port")
        )
        connector.connect()
        return connector
    except Exception as e:
        print("An error occurred while connecting to PostgreSQL:", e)
        return None

def process_all_java_files(directory, tablescolumns_dict):
    # 遍历指定目录下的所有文件和子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):  # 如果文件是 Java 文件
                file_path = os.path.join(root, file)
                parse_java_file(file_path, tablescolumns_dict)

def parse_java_file(file_path, tablescolumns_dict):
    parser = JavaASTParser(file_path, tablescolumns_dict)
    parser.parse()

def findAllTablesColumns(connection):
    # Example query execution
    result = connection.execute_query(CONFIG_INFO.get("findalltablescolumns"))
    resultList = list(result)
    tablescolumns_dict = {}
    for result in resultList:
        table_name = result[2]
        column_name = result[3]
        udt_name = result[27]

        if tablescolumns_dict.get(table_name) is not None:
            get = tablescolumns_dict.get(table_name)
            get[column_name] = udt_name
        else:
            columns_dict = {}
            columns_dict[column_name] = udt_name
            tablescolumns_dict[table_name] = columns_dict

    return tablescolumns_dict

def write_to_file(write_arr, file_name):
    if write_arr:
        with open(file_name + ".txt", "w", encoding="UTF-8") as file:
            for write_value in write_arr:
                file.write(write_value + "\n")

classcolumnsnotfindpostgres = []
postgrescolumnsnotfindclass = []
def submit():
    # 调用函数来获取连接对象
    connection = getPostgresConnect()
    # 获取所有表中得字段名
    tablescolumns_dict = findAllTablesColumns(connection)
    input_textnew = str(input_text.get()).replace("\\", "\\\\")
    process_all_java_files(input_textnew, tablescolumns_dict)
    write_to_file(classcolumnsnotfindpostgres, "ClassColumnsNotFindPostgres")
    write_to_file(postgrescolumnsnotfindclass, "PostgresColumnsNotFindClass")

# 读取配置文件
config = ConfigParser()
config.read('config_postgres.ini', encoding="UTF-8")
CONFIG_INFO = {}
for k, v in config['Config'].items():
    CONFIG_INFO[k] = v

# 创建根窗口
root = tk.Tk()
root.title("PostgresCompareJavabean")

# 设置窗口大小和背景颜色
window_width = 800
window_height = 500
root.geometry(f"{window_width}x{window_height}")  # 设置窗口大小为宽400像素，高300像素
root.configure(bg="#f0f0f0")  # 设置窗口背景颜色为浅灰色

# 创建输入框
input_text = tk.StringVar()  # 创建一个 StringVar 来存储输入框的值
input_text.set(r"D:\02_Project\96_Python")
input_box = tk.Entry(root, textvariable=input_text, width=130)  # 设置输入框宽度为 50 个字符
input_box.grid(row=0, column=0, padx=10, pady=10)  # 将输入框放置在第 0 行，第 0 列，并设置外边距


# 创建提交按钮
button_style = ttk.Style()
button_style.configure("TButton", font=("Arial", 12), background="#4CAF50", foreground="white", padding=10,
                       borderwidth=0, relief="flat", width=20, bordercolor="#4CAF50", focuscolor="#81C784")
submit_button = ttk.Button(root, text="提交", command=submit, style="TButton")  # 设置按钮样式
submit_button.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()
