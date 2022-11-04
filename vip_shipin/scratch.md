###打包前执行
pip install requests
pip freeze > requirements.txt

### 打包多个文件
pyinstaller -D -w vip_mian

### 打包单个文件
pyinstaller -F -w vip_mian

pyinstaller -i D:\Java\python\vip.ico -F -c D:\Java\python\vip_mian


pyinstaller -i D:\Java\python\vip.ico -F -c D:\Java\python\vip_mian
pyinstaller -i D:\Java\python\vip.ico -D -c D:\Java\python\vip_mian


pyinstaller -D D:\Java\python\vip_mian