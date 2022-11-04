import js2py
import json
from com.cll.io.FileIO import *

esprima = js2py.require('esprima')
escodegen = js2py.require('escodegen')

#js片段解析 start
str = "function _menuShow () {\
        $('nav a').addClass('menu-active');\
        $('.menu-bg').show();\
        $('.menu-item').css({opacity: 0});\
        TweenLite.to('.menu-container', 1, {padding: '0 40px'});\
        TweenLite.to('.menu-bg', 1, {opacity: '0.92'});\
        TweenMax.staggerTo('.menu-item', 0.5, {opacity: 1}, 0.3);\
        _menuOn = true;\
        $('.menu-bg').hover(function () {\
            $('nav a').toggleClass('menu-close-hover');\
        });\
        }"
tree = esprima.parse(str)
#js片段解析 end

#修改js属性值 start
tree.body[0].body.body[0].expression.arguments[0].value = "5555"
#修改js属性值 end

#读取js文件 start
fileDirName = "D:\sql"
arrayDate = []
arrayDate = get_fileName(fileDirName, ".js")
json_data_map = ''
for jsFile in arrayDate:
    with open(jsFile, 'r', encoding='utf-8') as f:
        json_data_map = f.read()
#读取js文件 end

#解析js文件 start
tree = esprima.parse(json_data_map)
print(json.dumps(tree.to_dict(), indent=4))
#解析js文件解析 end

#创建js start
generate = escodegen.generate(tree)
print(generate)
#创建js end