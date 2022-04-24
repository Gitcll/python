import os

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

#获取文件夹下所有的文件和数据
def get_file(path, fileNameSuffix):
    if os.path.exists(path):
        if os.path.isdir(path):
            sub_file = os.listdir(path)
            # 存放读取数据元组
            arrayData = []
            for file_name in sub_file:
                join_path = os.path.join(path, file_name)
                if os.path.isfile(join_path):
                    if os.path.splitext(join_path)[-1] == fileNameSuffix:
                        print(join_path)
                        arrayData = read_file_getArrayData(join_path)
                elif os.path.isdir(join_path):
                    get_file(join_path, fileNameSuffix)
        else:
            print("我要操作文件")
    else:
        print("该文件路径不存在")
    return arrayData

#获取文件夹下所有的文件
# 返回路径下指定fileName
fileNameArr = []
def get_fileName(path, fileNameSuffix):
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
        print("该文件路径不存在")
    return fileNameArr