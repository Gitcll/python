from com.cll.io.FileIO import *
import pandas as pd

path = "D:\\Java\\python\\resources\\"
fileDirectoryArr = []
fileDirectoryArr = get_directory(path)
for fileDirectory in fileDirectoryArr:
    fileNameArr = get_fileName(fileDirectory, ".java")
    contentList = []
    # mode='a'追加数据,mode='w'覆盖文件数据
    excelName = fileDirectory[str(fileDirectory).rindex("\\") + 1:]
    writer = pd.ExcelWriter(excelName + ".xlsx", mode='w', engine='openpyxl')
    for file in fileNameArr:
        contentList = read_file_getArrayData(file)
        print(contentList)
        i = 0
        blockMap = {}
        blockList = []
        startFlg = False
        fileName = file[str(file).rindex("\\")+1:].replace(".java", "")

        for content in contentList:
            if content.strip().startswith("//") and content.strip().endswith("start"):
                startFlg = True
                i += 1;
                continue
            if content.strip().startswith("//") and content.strip().endswith("end"):
                startFlg = False
                blockListNew = []
                blockListNewArr = []
                for blockContent in blockList:
                    if blockContent.strip().startswith("//"):
                        blockList.remove(blockContent)
                        blockListNew.append(blockContent)
                print(blockListNew)
                blockListNewArr.append(str(fileName))
                blockListNewArr.append(str(blockListNew).replace("['", "").replace("']", ""))
                blockListNewArr.append(str(blockList).replace("['", "").replace("']", ""))
                blockMap[str(fileName) + str(i)] = blockListNewArr
                blockList = []
                continue
            if startFlg:
                blockList.append(content)

        if len(blockMap) > 0:
            #dateArr11数据格式, 如: {"col1": [1, 2, 3], "col2": [4, 5, 6], "col3": [7, 8, 9]}
            #默认输出为竖向排列
            #T代表可以将数据横向排列,输出表格中
            data = pd.DataFrame(blockMap).T
            data = data.replace(r'\\n', '', regex=True)
            #写入数据
            data.to_excel(writer, sheet_name='sheet1', index=False)
            #保存excel,并关闭
            writer.close()
            fileNameArr.clear()
        print(content)