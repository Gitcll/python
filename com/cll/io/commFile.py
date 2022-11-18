import os
import chardet
import cchardet

#读取数据，存放入数组
def read_file_getArrayData(file):
    with open(file, 'r', encoding=get_encoding_cchardet(file)) as f:
        readlines = f.readlines()
        return readlines

# 获取文件编码类型
def get_encoding_chardet(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']

# 获取文件编码类型
def get_encoding_cchardet(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return cchardet.detect(f.read())['encoding']


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
                        fileNameArr.append(join_path)
                elif os.path.isdir(join_path):
                    get_fileName(join_path, fileNameSuffix)
        else:
            print("我要操作文件")
    else:
        print("该文件路径不存在")
    return fileNameArr