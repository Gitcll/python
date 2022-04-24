import javalang
from com.cll.io.FileIO import get_fileName
from javalang.ast import Node

def astNode(path, fileNameSuffix):
    fileNameArr = get_fileName(path, fileNameSuffix);
    for fileName in fileNameArr:
        with open(fileName, 'r', encoding='utf-8') as f:
            tree = javalang.parse.parse(f.read())
            print(type(tree.filter(javalang.tree.Declaration)), tree.filter(javalang.tree.Declaration))
            # 过滤不同类型的Declaration 过滤所有的方法：例如：tree.filter(javalang.tree.MethodDeclaration)
            tree_imports = tree.imports
            for importName in tree_imports:
                print(importName.path)

            for path, node in tree.filter(javalang.tree.MethodDeclaration):
                token = get_token(node)
                children = get_child(node)
                #print(token)
                #print(children)
                print(node)
            for path, node in tree.filter(javalang.tree.FieldDeclaration):
                print(node)

# 判断不同类型的Declaration
def get_token(node):
    token = ''
    if isinstance(node, Node):
        if isinstance(node, str):
            token = node
        elif isinstance(node, set):
            token = 'Modifier'
        elif isinstance(node, Node):
            token = node.__class__.__name__
    return token

# 获取类中子节点
def get_child(root):
    # print(root)
    if isinstance(root, Node):
        children = root.children
    elif isinstance(root, set):
        children = list(root)
    else:
        children = []

    def expand(nested_list):
        for item in nested_list:
            if isinstance(item, list):
                for sub_item in expand(item):
                    # print(sub_item)
                    yield sub_item
            elif item:
                # print(item)
                yield item

    return list(expand(children))