import pandas as pd

data = pd.DataFrame(
    {"col1":[1, 2, 3],
     "col2":[4, 5, 6],
     "col3":[7, 8, 9]
     }
    )
writer = pd.ExcelWriter("excel 样例.xlsx")
data.to_excel(writer, sheet_name="这是第一个sheet")
data.to_excel(writer, sheet_name="这是第二个sheet")
data.to_excel(writer, sheet_name="这是第三个sheet")
writer.save()
writer.close()