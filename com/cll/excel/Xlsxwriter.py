import xlsxwriter as xw

def xw_toExcel(data, fileName, sheetName):
    workbook = xw.Workbook(fileName)
    worksheet1 = workbook.add_worksheet(sheetName)
    worksheet1.activate()
    title = ['序号', '项目名', 'java包名', '覆盖率']
    worksheet1.write_row('A1', title)
    i = 2
    for j in range(len(data)):
        insertData = [1, data[j][0], data[j][0]]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    workbook.close()