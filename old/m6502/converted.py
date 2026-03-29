#"""
import json
string = ""
for opcode, data in opcodes.items():
    spec = data["newOpcode"].replace("([", "(").replace("])", ")")
    i = 0
    inputs = []
    for option in data["optionTypes"].keys():
        i += 1
        spec = spec.replace("["+option+"]", "%"+str(i))
        inputs.append("%m")
    for input in data["inputTypes"].keys():
        i += 1
        a = "("+input+")" 
        b = "<"+input+">"
        c = "{"+input+"}"
        #print("-", repr(spec), a, b, c)
        if c in spec:
            raise Exception()
        elif b in spec:
            spec = spec.replace(b, "%"+str(i))
            inputs.append("%b")
        elif a in spec:
            spec =  spec.replace(a, "%"+str(i))
            inputs.append("%n")
        else: raise Exception(input)
        #spec.replace(c, "%"+str(i))
    
    type = data["type"]
    if type == "stringReporter":
        shape = "reporter"
    elif type == "booleanReporter":
        shape = "boolean"
    elif type == "instruction":
        shape = "command"
    
    cat = opcode.split("_")[0]
    name = "_".join(opcode.split("_")[1:])
    string += "  {\n"
    string += "    id: " + json.dumps(cat+"."+name) + ",\n"
    string += "    spec: " + json.dumps(spec) + ",\n"
    string += "    inputs: " + json.dumps(inputs) + ",\n"
    string += "    shape: " + json.dumps(shape) + ",\n"
    string += "    category: " + json.dumps(cat) + ",\n"
    string += "  },\n" #"""
"""    string += {
  id: "jgJSON.json_combine",
  spec: "combine json %1 and json %2",
  inputs: ["%n", "%n"],
  shape: "reporter",
  category: "jgJSON",
}"""
print(string)
