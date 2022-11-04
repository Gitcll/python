import esprima
from com.cll.io.FileIO import *

#js行解析 start
program = 'const answer = 42'
returnTokenizeStr = esprima.tokenize(program)
returnParseScriptStr = esprima.parseScript(program)
returnParseModuleStr = esprima.parseModule(program)
#js行解析 end

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
returnTokenizeStr = esprima.tokenize(str)
returnParseScriptStr = esprima.parseScript(str)
returnParseModuleStr = esprima.parseModule(str)
#js片段解析 end

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
returnParseScriptStr = esprima.parseScript(json_data_map)
#解析js文件 end

print(returnParseScriptStr)

#判断js类型 start
for body in returnParseScriptStr.body:
    if body.type == 'FunctionDeclaration':
        print(body.type)
#判断js类型 start
