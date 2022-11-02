import esprima
from .visitor import NodeVisitor


program = 'const answer = 42'
returnTokenizeStr = esprima.tokenize(program)
returnParseScriptStr = esprima.parseScript(program)
returnParseModuleStr = esprima.parseModule(program);


#print(returnTokenizeStr)
#print(returnParseScriptStr)

