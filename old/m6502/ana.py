text = open("main.py").read()
lines = text.splitlines()

import ast
tree = ast.parse(text)
del tree.body[0]
del tree.body[0]
del tree.body[0]
#print(ast.dump(tree, indent=4)[:50000])

new = []
o = []
code = ""
for node in tree.body:
    if isinstance(node, ast.FunctionDef):
        if node.name.startswith("P_ins"):#node.name.endswith("_iny"):
            new.append(node)
            o.append(node.name.removeprefix("P_ins_"))
            #print(node.name, 100*"=")
            #print(node.lineno, node.end_lineno)
            #seg ="\n".join(lines[node.lineno-1:node.end_lineno+1])
            #seg ="\n".join(lines[node.lineno-1:node.lineno]+[""])
            #code += seg
            #print(seg)
print(o)
new_module = ast.Module(new)
#print(ast.dump(new_module, indent=4))
#print(code)
