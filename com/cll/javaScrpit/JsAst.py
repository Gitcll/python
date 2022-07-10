import js2py
import json

esprima = js2py.require('esprima')
escodegen = js2py.require('escodegen')

str = 'function onchangeHiddenMultiple(checkbox, checkboxHidden){\
	//var allCheckChanges = document.getElementsByClassName(checkboxHidden);\
	var input = document.getElementsByTagName("input");\
	$.each(input,function(index,obj){\
		var checkboxId = document.getElementById(checkbox+"_"+index);\
		if(checkboxId != undefined && checkboxId != null){\
			if(input[index].value == "true"){\
				document.getElementById(checkbox+"_"+index).checked = true;\
			}else{\
				document.getElementById(checkbox+"_"+index).checked = false;\
			}\
		}\
	});\
}'
tree = esprima.parse(str)
print(json.dumps(tree.to_dict(), indent=4))
tree.body
print(esprima)